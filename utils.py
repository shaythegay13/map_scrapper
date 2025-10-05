"""
Utility functions for data normalization and geocoding
"""

import re
from typing import Optional, Dict, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataNormalizer:
    """Normalize and standardize scraped data"""
    
    @staticmethod
    def normalize_phone(phone: Optional[str]) -> Optional[str]:
        """Normalize phone number format"""
        if not phone:
            return None
        
        # Remove all non-numeric characters
        digits = re.sub(r'\D', '', phone)
        
        # Format as (XXX) XXX-XXXX if 10 digits
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        
        return phone
    
    @staticmethod
    def normalize_address(address: Optional[str]) -> Optional[str]:
        """Clean and normalize address"""
        if not address:
            return None
        
        # Remove extra whitespace
        address = ' '.join(address.split())
        
        # Standardize common abbreviations
        replacements = {
            r'\bSt\b': 'Street',
            r'\bAve\b': 'Avenue',
            r'\bRd\b': 'Road',
            r'\bBlvd\b': 'Boulevard',
            r'\bDr\b': 'Drive',
            r'\bLn\b': 'Lane',
            r'\bPl\b': 'Place',
            r'\bCt\b': 'Court',
        }
        
        for pattern, replacement in replacements.items():
            address = re.sub(pattern, replacement, address, flags=re.IGNORECASE)
        
        return address
    
    @staticmethod
    def extract_neighborhood(address: str) -> Optional[str]:
        """Extract neighborhood from address if present"""
        # Common NYC borough/neighborhood patterns
        boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
        
        for borough in boroughs:
            if borough.lower() in address.lower():
                return borough
        
        return None
    
    @staticmethod
    def normalize_hours(hours: Optional[str]) -> Optional[str]:
        """Normalize operating hours format"""
        if not hours:
            return None
        
        # Remove extra whitespace
        hours = ' '.join(hours.split())
        
        return hours
    
    @staticmethod
    def extract_social_media(text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract social media links from text"""
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        
        website1 = urls[0] if len(urls) > 0 else None
        website2 = urls[1] if len(urls) > 1 else None
        
        return website1, website2


class Geocoder:
    """Geocode addresses to lat/long coordinates"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="nyc_food_access_scraper")
        self.cache = {}
    
    def geocode(self, address: str, max_retries: int = 3) -> Optional[Tuple[float, float]]:
        """
        Geocode an address to lat/long coordinates
        
        Args:
            address: Address string to geocode
            max_retries: Maximum number of retry attempts
            
        Returns:
            Tuple of (latitude, longitude) or None if geocoding fails
        """
        if not address:
            return None
        
        # Check cache first
        if address in self.cache:
            return self.cache[address]
        
        for attempt in range(max_retries):
            try:
                # Add NYC context to improve accuracy
                search_address = f"{address}, New York"
                
                location = self.geolocator.geocode(search_address, timeout=10)
                
                if location:
                    coords = (location.latitude, location.longitude)
                    self.cache[address] = coords
                    logger.info(f"Geocoded: {address} -> {coords}")
                    return coords
                else:
                    logger.warning(f"No geocoding result for: {address}")
                    return None
                    
            except GeocoderTimedOut:
                logger.warning(f"Geocoding timeout for {address}, attempt {attempt + 1}/{max_retries}")
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except GeocoderServiceError as e:
                logger.error(f"Geocoding service error for {address}: {e}")
                return None
        
        logger.error(f"Failed to geocode after {max_retries} attempts: {address}")
        return None
    
    def is_within_bounds(self, lat: float, lon: float) -> bool:
        """
        Check if coordinates are within the target geographic area
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            True if within bounds, False otherwise
        """
        # Approximate bounds for NYC + surrounding areas
        # NYC: ~40.4774° to 40.9176° N, -74.2591° to -73.7004° W
        # Extended for Westchester, Long Island, and NJ
        
        min_lat, max_lat = 40.0, 41.5  # Covers NYC to Westchester
        min_lon, max_lon = -74.8, -71.8  # Covers NJ to Long Island
        
        return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon


def create_data_record(
    name: Optional[str] = None,
    address: Optional[str] = None,
    neighborhood: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    description: Optional[str] = None,
    data_type: Optional[str] = None,
    open_hours: Optional[str] = None,
    owner: Optional[str] = None,
    local_items: Optional[str] = None,
    contact: Optional[str] = None,
    website1: Optional[str] = None,
    website2: Optional[str] = None,
    source_url: Optional[str] = None
) -> Dict:
    """
    Create a standardized data record
    
    Returns:
        Dictionary with all required fields
    """
    from datetime import datetime
    
    normalizer = DataNormalizer()
    
    return {
        "name": name,
        "address": normalizer.normalize_address(address) if address else None,
        "neighborhood": neighborhood or (normalizer.extract_neighborhood(address) if address else None),
        "lat": lat,
        "long": lon,
        "description": description,
        "type": data_type,
        "open_hours": normalizer.normalize_hours(open_hours),
        "owner": owner,
        "local_items_selling": local_items,
        "contact_information": normalizer.normalize_phone(contact) if contact else None,
        "social_media_website1": website1,
        "social_media_website2": website2,
        "source_url": source_url,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
