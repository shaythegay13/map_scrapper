"""
Scraper for API-based data sources (NYC Open Data, etc.)
"""

import requests
import logging
from typing import List, Dict, Optional
from .base_scraper import BaseScraper
from utils import create_data_record, Geocoder

logger = logging.getLogger(__name__)


class APIScraper(BaseScraper):
    """Scraper for API endpoints, especially Socrata (NYC Open Data)"""
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.api_format = source_config.get('format', 'json')
        self.geocoder = Geocoder()
    
    def scrape(self) -> List[Dict]:
        """Scrape data from API endpoint"""
        
        if self.api_format == 'socrata_api':
            return self.scrape_socrata()
        else:
            return self.scrape_generic_api()
    
    def scrape_socrata(self) -> List[Dict]:
        """
        Scrape NYC Open Data Socrata API
        
        Returns:
            List of data records
        """
        results = []
        limit = 1000
        offset = 0
        
        try:
            while True:
                # Socrata API pagination
                params = {
                    '$limit': limit,
                    '$offset': offset,
                    '$order': ':id'
                }
                
                response = self.session.get(self.url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if not data:
                    break
                
                logger.info(f"Processing {len(data)} records from offset {offset}")
                
                for item in data:
                    record = self.parse_socrata_record(item)
                    if record:
                        results.append(record)
                
                if len(data) < limit:
                    break
                
                offset += limit
        
        except Exception as e:
            logger.error(f"Error scraping Socrata API {self.url}: {e}")
        
        return results
    
    def parse_socrata_record(self, item: Dict) -> Optional[Dict]:
        """
        Parse a single record from Socrata API
        
        Args:
            item: Raw API record
            
        Returns:
            Normalized data record
        """
        try:
            # Extract coordinates
            lat, lon = None, None
            
            # Try different coordinate field names
            if 'latitude' in item and 'longitude' in item:
                lat = float(item['latitude'])
                lon = float(item['longitude'])
            elif 'lat' in item and 'lon' in item:
                lat = float(item['lat'])
                lon = float(item['lon'])
            elif 'location' in item and isinstance(item['location'], dict):
                lat = float(item['location'].get('latitude', 0))
                lon = float(item['location'].get('longitude', 0))
            elif 'the_geom' in item and isinstance(item['the_geom'], dict):
                coords = item['the_geom'].get('coordinates', [])
                if len(coords) >= 2:
                    lon, lat = coords[0], coords[1]
            
            # If no coordinates, try geocoding the address
            address = (item.get('address') or 
                      item.get('street_address') or 
                      item.get('location_1') or
                      item.get('location'))
            if not lat and address:
                coords = self.geocoder.geocode(address)
                if coords:
                    lat, lon = coords
            
            # Extract other fields
            name = (item.get('gardenname') or  # GreenThumb specific
                   item.get('garden_name') or 
                   item.get('name') or 
                   item.get('site_name') or 
                   item.get('facility_name') or
                   item.get('food_scrap_drop_off_site') or
                   item.get('hosted_by'))
            
            # Decode borough codes for GreenThumb data
            borough_code = item.get('borough')
            if borough_code:
                borough_map = {
                    'M': 'Manhattan',
                    'B': 'Brooklyn', 
                    'Q': 'Queens',
                    'X': 'Bronx',
                    'R': 'Staten Island'
                }
                neighborhood = borough_map.get(borough_code, borough_code)
            else:
                neighborhood = (item.get('neighborhood') or 
                              item.get('community_board'))
            
            # Combine hours from GreenThumb (has separate fields for each day)
            hours_parts = []
            day_fields = [
                ('Mon', item.get('openhrsm')),
                ('Tue', item.get('openhrstu')),
                ('Wed', item.get('openhrsw')),
                ('Thu', item.get('openhrsth')),
                ('Fri', item.get('openhrsf')),
                ('Sat', item.get('openhrssa')),
                ('Sun', item.get('openhrssu'))
            ]
            for day, hrs in day_fields:
                if hrs and hrs.lower() != 'closed':
                    hours_parts.append(f"{day}: {hrs}")
            
            hours = '; '.join(hours_parts) if hours_parts else None
            
            # Fallback to other hour fields
            if not hours:
                hours = (item.get('operation_day_hours') or
                        item.get('hours') or
                        item.get('open_months'))
            
            # Owner/jurisdiction
            owner = item.get('juris') or item.get('owner')
            
            # Cross streets for additional location info
            cross_streets = item.get('crossstreets')
            description = cross_streets or item.get('notes') or item.get('description')
            
            contact = (item.get('contact_phone') or 
                      item.get('phone') or 
                      item.get('telephone'))
            
            website = item.get('website') or item.get('url')
            
            return create_data_record(
                name=name,
                address=address,
                neighborhood=neighborhood,
                lat=lat,
                lon=lon,
                description=description,
                data_type=self.data_type,
                open_hours=hours,
                owner=owner,
                contact=contact,
                website1=website,
                source_url=self.url
            )
        
        except Exception as e:
            logger.error(f"Error parsing Socrata record: {e}")
            return None
    
    def scrape_generic_api(self) -> List[Dict]:
        """
        Scrape generic JSON API
        
        Returns:
            List of data records
        """
        results = []
        
        try:
            response = self.get_page(self.url)
            if not response:
                return results
            
            data = response.json()
            
            # Handle different JSON structures
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                # Try common keys for data arrays
                items = (data.get('data') or 
                        data.get('results') or 
                        data.get('items') or 
                        [data])
            else:
                logger.warning(f"Unexpected JSON structure from {self.url}")
                return results
            
            for item in items:
                # Generic parsing - adapt as needed
                record = create_data_record(
                    name=item.get('name'),
                    address=item.get('address'),
                    lat=item.get('latitude') or item.get('lat'),
                    lon=item.get('longitude') or item.get('lon'),
                    description=item.get('description'),
                    data_type=self.data_type,
                    source_url=self.url
                )
                results.append(record)
        
        except Exception as e:
            logger.error(f"Error scraping generic API {self.url}: {e}")
        
        return results
