"""
Scraper for HTML-based websites
"""

import re
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from utils import create_data_record, Geocoder

logger = logging.getLogger(__name__)


class HTMLScraper(BaseScraper):
    """Scraper for HTML websites"""
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.geocoder = Geocoder()
    
    def scrape(self) -> List[Dict]:
        """Main scraping method - routes to specific scrapers based on domain"""
        
        # Route to specific scraper based on URL
        if 'nycgovparks.org' in self.url:
            return self.scrape_nyc_parks()
        elif 'lungsnyc.org' in self.url:
            return self.scrape_lungs_nyc()
        elif 'communityfridgefinder.com' in self.url:
            return self.scrape_fridge_finder()
        elif 'onelovecommunityfridge.org' in self.url:
            return self.scrape_one_love()
        elif 'manhattanlandtrust.org' in self.url or 'bqlt.org' in self.url or 'bronxlandtrust.org' in self.url:
            return self.scrape_land_trust()
        elif 'nyrp.org' in self.url:
            return self.scrape_nyrp()
        elif 'foodbanknyc.org' in self.url:
            return self.scrape_food_bank_nyc()
        elif 'cityharvest.org' in self.url:
            return self.scrape_city_harvest()
        elif 'grownyc.org' in self.url:
            return self.scrape_grownyc()
        elif 'localharvest.org' in self.url:
            return self.scrape_local_harvest()
        else:
            return self.scrape_generic()
    
    def scrape_nyc_parks(self) -> List[Dict]:
        """Scrape NYC Parks GreenThumb community gardens"""
        results = []
        
        response = self.get_page(self.url)
        if not response:
            return results
        
        soup = self.parse_html(response.text)
        if not soup:
            return results
        
        # Find garden listings - adjust selectors based on actual HTML structure
        gardens = soup.select('.garden-item, .location-item, article, .view-content .views-row')
        
        for garden in gardens:
            try:
                name = garden.select_one('h2, h3, .title, .garden-name')
                name = name.get_text(strip=True) if name else None
                
                address_elem = garden.select_one('.address, .location, .field-address')
                address = address_elem.get_text(strip=True) if address_elem else None
                
                description_elem = garden.select_one('.description, .body, .field-body')
                description = description_elem.get_text(strip=True) if description_elem else None
                
                # Try to find contact info
                contact = None
                phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', garden.get_text())
                if phone_match:
                    contact = phone_match.group()
                
                # Geocode if we have an address
                lat, lon = None, None
                if address:
                    coords = self.geocoder.geocode(address)
                    if coords:
                        lat, lon = coords
                
                if name:
                    record = create_data_record(
                        name=name,
                        address=address,
                        lat=lat,
                        lon=lon,
                        description=description,
                        data_type=self.data_type,
                        contact=contact,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing garden item: {e}")
                continue
        
        return results
    
    def scrape_lungs_nyc(self) -> List[Dict]:
        """Scrape LUNGS NYC gardens"""
        results = []
        
        response = self.get_page(self.url)
        if not response:
            return results
        
        soup = self.parse_html(response.text)
        if not soup:
            return results
        
        # Adjust selectors based on actual site structure
        items = soup.select('.garden, .location, article, .wp-block-group')
        
        for item in items:
            try:
                name = item.select_one('h1, h2, h3, h4, .title')
                name = name.get_text(strip=True) if name else None
                
                # Extract all text and look for address patterns
                text = item.get_text()
                
                # Look for NYC address pattern
                address_match = re.search(r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Place|Pl)[,\s]+(?:Brooklyn|Manhattan|Queens|Bronx|Staten Island)', text, re.IGNORECASE)
                address = address_match.group() if address_match else None
                
                if name:
                    lat, lon = None, None
                    if address:
                        coords = self.geocoder.geocode(address)
                        if coords:
                            lat, lon = coords
                    
                    record = create_data_record(
                        name=name,
                        address=address,
                        lat=lat,
                        lon=lon,
                        data_type=self.data_type,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing LUNGS item: {e}")
                continue
        
        return results
    
    def scrape_fridge_finder(self) -> List[Dict]:
        """Scrape Community Fridge Finder"""
        results = []
        
        response = self.get_page(self.url)
        if not response:
            return results
        
        soup = self.parse_html(response.text)
        if not soup:
            return results
        
        # Look for fridge listings
        fridges = soup.select('.fridge-item, .location, .listing-item, article')
        
        for fridge in fridges:
            try:
                name = fridge.select_one('h2, h3, h4, .name, .title')
                name = name.get_text(strip=True) if name else None
                
                address_elem = fridge.select_one('.address, .location')
                address = address_elem.get_text(strip=True) if address_elem else None
                
                hours_elem = fridge.select_one('.hours, .open-hours, .schedule')
                hours = hours_elem.get_text(strip=True) if hours_elem else None
                
                if name or address:
                    lat, lon = None, None
                    if address:
                        coords = self.geocoder.geocode(address)
                        if coords:
                            lat, lon = coords
                    
                    record = create_data_record(
                        name=name or "Community Fridge",
                        address=address,
                        lat=lat,
                        lon=lon,
                        data_type=self.data_type,
                        open_hours=hours,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing fridge item: {e}")
                continue
        
        return results
    
    def scrape_one_love(self) -> List[Dict]:
        """Scrape One Love Community Fridge"""
        return self.scrape_fridge_finder()  # Similar structure
    
    def scrape_land_trust(self) -> List[Dict]:
        """Scrape land trust gardens (Manhattan, Brooklyn-Queens, Bronx)"""
        results = []
        
        response = self.get_page(self.url)
        if not response:
            return results
        
        soup = self.parse_html(response.text)
        if not soup:
            return results
        
        gardens = soup.select('.garden, .site, article, .wp-block-column')
        
        for garden in gardens:
            try:
                name = garden.select_one('h2, h3, h4, .title, strong')
                name = name.get_text(strip=True) if name else None
                
                # Get all text content
                text = garden.get_text()
                
                # Extract address
                address_match = re.search(r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)', text, re.IGNORECASE)
                address = address_match.group() if address_match else None
                
                # Extract phone
                phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
                contact = phone_match.group() if phone_match else None
                
                # Extract email
                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
                if email_match and not contact:
                    contact = email_match.group()
                
                if name:
                    lat, lon = None, None
                    if address:
                        coords = self.geocoder.geocode(address)
                        if coords:
                            lat, lon = coords
                    
                    record = create_data_record(
                        name=name,
                        address=address,
                        lat=lat,
                        lon=lon,
                        data_type=self.data_type,
                        contact=contact,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing land trust garden: {e}")
                continue
        
        return results
    
    def scrape_nyrp(self) -> List[Dict]:
        """Scrape NYRP gardens and parks"""
        return self.scrape_land_trust()  # Similar structure
    
    def scrape_food_bank_nyc(self) -> List[Dict]:
        """Scrape Food Bank NYC locations"""
        results = []
        
        response = self.get_page(self.url)
        if not response:
            return results
        
        soup = self.parse_html(response.text)
        if not soup:
            return results
        
        locations = soup.select('.location, .site, .pantry, article')
        
        for location in locations:
            try:
                name = location.select_one('h2, h3, h4, .title, .name')
                name = name.get_text(strip=True) if name else None
                
                address_elem = location.select_one('.address, .location-address')
                address = address_elem.get_text(strip=True) if address_elem else None
                
                hours_elem = location.select_one('.hours, .schedule')
                hours = hours_elem.get_text(strip=True) if hours_elem else None
                
                phone_elem = location.select_one('.phone, .telephone')
                contact = phone_elem.get_text(strip=True) if phone_elem else None
                
                if name or address:
                    lat, lon = None, None
                    if address:
                        coords = self.geocoder.geocode(address)
                        if coords:
                            lat, lon = coords
                    
                    record = create_data_record(
                        name=name or "Food Bank Location",
                        address=address,
                        lat=lat,
                        lon=lon,
                        data_type=self.data_type,
                        open_hours=hours,
                        contact=contact,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing food bank location: {e}")
                continue
        
        return results
    
    def scrape_city_harvest(self) -> List[Dict]:
        """Scrape City Harvest food map"""
        return self.scrape_food_bank_nyc()  # Similar structure
    
    def scrape_grownyc(self) -> List[Dict]:
        """Scrape GrowNYC greenmarkets"""
        results = []
        
        response = self.get_page(self.url)
        if not response:
            return results
        
        soup = self.parse_html(response.text)
        if not soup:
            return results
        
        markets = soup.select('.market, .location, article, .view-row')
        
        for market in markets:
            try:
                name = market.select_one('h2, h3, .title, .market-name')
                name = name.get_text(strip=True) if name else None
                
                address_elem = market.select_one('.address, .location')
                address = address_elem.get_text(strip=True) if address_elem else None
                
                hours_elem = market.select_one('.hours, .schedule, .days')
                hours = hours_elem.get_text(strip=True) if hours_elem else None
                
                if name:
                    lat, lon = None, None
                    if address:
                        coords = self.geocoder.geocode(address)
                        if coords:
                            lat, lon = coords
                    
                    record = create_data_record(
                        name=name,
                        address=address,
                        lat=lat,
                        lon=lon,
                        data_type=self.data_type,
                        open_hours=hours,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing market: {e}")
                continue
        
        return results
    
    def scrape_local_harvest(self) -> List[Dict]:
        """Scrape Local Harvest listings (CSAs, farms, markets)"""
        results = []
        
        response = self.get_page(self.url)
        if not response:
            return results
        
        soup = self.parse_html(response.text)
        if not soup:
            return results
        
        # Local Harvest uses div.membercell for listings
        listings = soup.select('div.membercell')
        
        logger.info(f"Found {len(listings)} Local Harvest listings")
        
        for listing in listings:
            try:
                # Name is in an <a> tag with class mt-0
                name_elem = listing.select_one('a.mt-0')
                name = name_elem.get_text(strip=True) if name_elem else None
                
                # Location is in a link with pattern /city-state
                location_elem = listing.select_one('a[href*="-ny"], a[href*="-nj"]')
                location = location_elem.get_text(strip=True) if location_elem else None
                
                # Description
                desc_elem = listing.select_one('p.d-none')
                description = desc_elem.get_text(strip=True) if desc_elem else None
                
                # Build address from location (city, state)
                address = location if location else None
                
                if name:
                    lat, lon = None, None
                    if address:
                        coords = self.geocoder.geocode(address + ", USA")
                        if coords:
                            lat, lon = coords
                    
                    record = create_data_record(
                        name=name,
                        address=address,
                        lat=lat,
                        lon=lon,
                        description=description,
                        data_type=self.data_type,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing Local Harvest listing: {e}")
                continue
        
        return results
    
    def scrape_generic(self) -> List[Dict]:
        """Generic scraper for unknown sites"""
        results = []
        
        response = self.get_page(self.url)
        if not response:
            return results
        
        soup = self.parse_html(response.text)
        if not soup:
            return results
        
        # Try common selectors
        items = soup.select('article, .location, .item, .entry, .post')
        
        for item in items:
            try:
                # Try to find name
                name = item.select_one('h1, h2, h3, h4, .title, .name')
                name = name.get_text(strip=True) if name else None
                
                # Try to find address in text
                text = item.get_text()
                address_match = re.search(r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd)', text, re.IGNORECASE)
                address = address_match.group() if address_match else None
                
                if name or address:
                    lat, lon = None, None
                    if address:
                        coords = self.geocoder.geocode(address)
                        if coords:
                            lat, lon = coords
                    
                    record = create_data_record(
                        name=name,
                        address=address,
                        lat=lat,
                        lon=lon,
                        data_type=self.data_type,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error in generic scraper: {e}")
                continue
        
        return results
