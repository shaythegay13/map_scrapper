"""
Scraper for map-based data sources (ArcGIS, Google Maps)
"""

import requests
import json
import logging
from typing import List, Dict
from .base_scraper import BaseScraper
from utils import create_data_record, Geocoder

logger = logging.getLogger(__name__)


class MapScraper(BaseScraper):
    """Scraper for map data sources"""
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.map_format = source_config.get('format', 'unknown')
        self.geocoder = Geocoder()
    
    def scrape(self) -> List[Dict]:
        """Main scraping method - routes to specific scrapers based on format"""
        
        if self.map_format == 'arcgis':
            return self.scrape_arcgis()
        elif self.map_format == 'google_maps':
            return self.scrape_google_maps()
        else:
            logger.warning(f"Unknown map format: {self.map_format}")
            return []
    
    def scrape_arcgis(self) -> List[Dict]:
        """
        Scrape ArcGIS dashboard/feature service
        
        ArcGIS dashboards typically expose data through REST API endpoints
        """
        results = []
        
        try:
            # For NYC ArcGIS dashboards, the data is usually in NYC Open Data
            # The dashboard at https://nyc.maps.arcgis.com/apps/dashboards/7d3e668dfcdd4bce93275dae44fcd3dd
            # displays GreenThumb garden data which we already get from the API
            
            if 'nyc.maps.arcgis.com' in self.url:
                logger.info("NYC ArcGIS dashboard detected - data available through NYC Open Data API")
                logger.info("This dashboard displays GreenThumb gardens (already scraped via API)")
                logger.info("Plus additional urban agriculture sites from various sources")
                
                # Try multiple potential endpoints
                potential_endpoints = [
                    # GreenThumb gardens (already in API but try anyway)
                    "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/GreenThumb_Garden_Info/FeatureServer/0/query",
                    # Try generic urban agriculture
                    "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/Urban_Agriculture/FeatureServer/0/query",
                    # Try food access
                    "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/Food_Access/FeatureServer/0/query",
                ]
                
                for api_url in potential_endpoints:
                    try:
                        params = {
                            'where': '1=1',
                            'outFields': '*',
                            'f': 'json',
                            'resultRecordCount': 2000,
                            'returnGeometry': 'true'
                        }
                        
                        logger.info(f"Trying ArcGIS endpoint: {api_url}")
                        response = self.session.get(api_url, params=params, timeout=30)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            if 'features' in data and len(data['features']) > 0:
                                logger.info(f"✓ Found {len(data['features'])} features from {api_url}")
                                
                                for feature in data['features']:
                                    record = self.parse_arcgis_feature(feature)
                                    if record:
                                        results.append(record)
                                break  # Found data, stop trying
                            else:
                                logger.debug(f"No features at {api_url}")
                        else:
                            logger.debug(f"Endpoint not available: {api_url} (status {response.status_code})")
                    
                    except Exception as e:
                        logger.debug(f"Failed to query {api_url}: {e}")
                        continue
                
                if not results:
                    logger.warning("Could not find ArcGIS feature service endpoint - data may require dashboard interaction")
                    logger.info("Note: The 1000+ count may include data from multiple sources aggregated in the dashboard")
            
        except Exception as e:
            logger.error(f"Error scraping ArcGIS {self.url}: {e}")
        
        return results
    
    def parse_arcgis_feature(self, feature: Dict) -> Dict:
        """Parse a single ArcGIS feature"""
        try:
            attributes = feature.get('attributes', {})
            geometry = feature.get('geometry', {})
            
            # Extract coordinates
            lat = geometry.get('y') or geometry.get('latitude')
            lon = geometry.get('x') or geometry.get('longitude')
            
            # Extract attributes (field names vary by dataset)
            name = (attributes.get('name') or 
                   attributes.get('NAME') or 
                   attributes.get('GardenName') or
                   attributes.get('GARDEN_NAME') or
                   attributes.get('SiteName'))
            
            address = (attributes.get('address') or 
                      attributes.get('ADDRESS') or 
                      attributes.get('Address') or
                      attributes.get('LOCATION'))
            
            neighborhood = (attributes.get('borough') or 
                          attributes.get('BOROUGH') or
                          attributes.get('neighborhood') or
                          attributes.get('NEIGHBORHOOD'))
            
            description = (attributes.get('description') or
                         attributes.get('DESCRIPTION') or
                         attributes.get('notes') or
                         attributes.get('NOTES'))
            
            return create_data_record(
                name=name,
                address=address,
                neighborhood=neighborhood,
                lat=lat,
                lon=lon,
                description=description,
                data_type=self.data_type,
                source_url=self.url
            )
        
        except Exception as e:
            logger.error(f"Error parsing ArcGIS feature: {e}")
            return None
    
    def scrape_google_maps(self) -> List[Dict]:
        """
        Scrape Google My Maps
        
        Google My Maps data can sometimes be accessed via KML export
        """
        results = []
        
        try:
            # Extract the map ID from URL
            import re
            mid_match = re.search(r'mid=([^&]+)', self.url)
            
            if mid_match:
                mid = mid_match.group(1)
                
                # Try to get KML export
                kml_url = f"https://www.google.com/maps/d/u/0/kml?mid={mid}&forcekml=1"
                
                response = self.get_page(kml_url)
                if not response:
                    logger.warning(f"Could not access Google Maps KML for {self.name}")
                    return results
                
                # Parse KML (would need additional library)
                # For now, log that this needs manual handling
                logger.warning(f"Google Maps scraping requires KML parsing - not yet implemented for {self.name}")
                logger.info(f"KML URL: {kml_url}")
                
        except Exception as e:
            logger.error(f"Error scraping Google Maps {self.url}: {e}")
        
        return results
