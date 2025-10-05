"""
Base scraper class with common functionality
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Optional
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers"""
    
    def __init__(self, source_config: Dict):
        """
        Initialize scraper with source configuration
        
        Args:
            source_config: Dictionary containing source metadata
        """
        self.name = source_config.get('name', 'Unknown')
        self.url = source_config.get('url')
        self.data_type = source_config.get('type')
        self.source_config = source_config
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def get_page(self, url: str, timeout: int = 30) -> Optional[requests.Response]:
        """
        Fetch a web page with error handling
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            Response object or None if request fails
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            time.sleep(2)  # Rate limiting
            return response
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html_content: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content
        
        Args:
            html_content: Raw HTML string
            
        Returns:
            BeautifulSoup object or None
        """
        try:
            return BeautifulSoup(html_content, 'lxml')
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Main scraping method - must be implemented by subclasses
        
        Returns:
            List of data records
        """
        pass
    
    def run(self) -> List[Dict]:
        """
        Execute the scraper with error handling
        
        Returns:
            List of scraped data records
        """
        try:
            logger.info(f"Starting scraper: {self.name}")
            data = self.scrape()
            logger.info(f"Completed scraper: {self.name} - Found {len(data)} records")
            return data
        except Exception as e:
            logger.error(f"Error in scraper {self.name}: {e}", exc_info=True)
            return []
