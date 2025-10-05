"""
Selenium-based scraper for JavaScript-heavy websites
"""

import logging
import time
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper
from utils import create_data_record, Geocoder

logger = logging.getLogger(__name__)


class SeleniumScraper(BaseScraper):
    """Scraper for JavaScript-heavy websites using Selenium"""
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.geocoder = Geocoder()
        self.driver = None
    
    def setup_driver(self):
        """Initialize Selenium WebDriver with Chrome"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Try to use chromedriver
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info("Chrome WebDriver initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Chrome WebDriver: {e}")
                logger.info("Install ChromeDriver: https://chromedriver.chromium.org/")
                raise
            
        except Exception as e:
            logger.error(f"Error setting up Selenium driver: {e}")
            raise
    
    def teardown_driver(self):
        """Close Selenium WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chrome WebDriver closed")
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
    
    def scrape(self) -> List[Dict]:
        """Main scraping method using Selenium"""
        results = []
        
        try:
            self.setup_driver()
            
            # Route to specific scraper based on URL
            if 'finder.nyc.gov' in self.url:
                results = self.scrape_nyc_food_finder()
            elif 'cityharvest.org' in self.url:
                results = self.scrape_city_harvest()
            elif 'google.com/maps' in self.url:
                results = self.scrape_google_maps()
            elif 'arcgis.com' in self.url:
                results = self.scrape_arcgis_dashboard()
            else:
                results = self.scrape_generic_js_site()
            
        except Exception as e:
            logger.error(f"Error in Selenium scraper for {self.name}: {e}")
        
        finally:
            self.teardown_driver()
        
        return results
    
    def scrape_nyc_food_finder(self) -> List[Dict]:
        """Scrape NYC Food Help Finder (JavaScript-based map)"""
        results = []
        
        try:
            logger.info(f"Loading {self.url} with Selenium...")
            self.driver.get(self.url)
            
            # Wait for initial load
            time.sleep(10)
            
            # Try to click "Load All" button to get all locations
            try:
                load_all_button = self.driver.find_element(By.ID, 'load-all-btn')
                logger.info("Clicking 'Load All' button...")
                load_all_button.click()
                time.sleep(15)  # Wait for all locations to load
            except Exception as e:
                logger.warning(f"Could not click Load All button: {e}")
            
            # Get page source after all locations loaded
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Find all location items with data-locationid
            location_items = soup.select('li[data-locationid]')
            
            logger.info(f"Found {len(location_items)} food assistance locations")
            
            for item in location_items:
                try:
                    # Extract name from h3 tag
                    name_elem = item.select_one('h3')
                    name = name_elem.get_text(strip=True) if name_elem else None
                    
                    # Extract address from the specific span after h3
                    address = None
                    # Address is in first p tag after h3, in a span
                    address_p = item.select('p.sc-kAyceB')[0] if item.select('p.sc-kAyceB') else None
                    if address_p:
                        address_span = address_p.select_one('span')
                        if address_span:
                            address = address_span.get_text(strip=True)
                    
                    # Try to extract coordinates from Google Maps link
                    lat, lon = None, None
                    maps_link = item.select_one('a[href*="google.com/maps"]')
                    if maps_link:
                        href = maps_link.get('href', '')
                        # Extract coordinates from URL like: destination=40.734195062000026%2C-73.99571909299999
                        import re
                        coords_match = re.search(r'destination=([\d.-]+)%2C([\d.-]+)', href)
                        if coords_match:
                            lat = float(coords_match.group(1))
                            lon = float(coords_match.group(2))
                    
                    # If no coordinates from link, try geocoding
                    if not lat and address:
                        coords = self.geocoder.geocode(address)
                        if coords:
                            lat, lon = coords
                    
                    if name or address:
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
                    logger.error(f"Error parsing food location: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error scraping NYC Food Finder: {e}")
        
        return results
    
    def scrape_city_harvest(self) -> List[Dict]:
        """Scrape City Harvest food map"""
        results = []
        
        try:
            logger.info(f"Loading {self.url} with Selenium...")
            self.driver.get(self.url)
            
            # Wait for map to load
            time.sleep(5)
            
            # Try to find and click "List View" if available
            try:
                list_button = self.driver.find_element(By.XPATH, "//*[contains(text(), 'List') or contains(text(), 'list')]")
                list_button.click()
                time.sleep(2)
            except:
                pass
            
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Look for food bank/pantry listings
            locations = soup.select('.location, .pantry, .site, article, [class*="location"]')
            
            logger.info(f"Found {len(locations)} potential locations")
            
            for location in locations:
                try:
                    name = location.select_one('h1, h2, h3, h4, .name, .title')
                    name = name.get_text(strip=True) if name else None
                    
                    address_elem = location.select_one('.address, [class*="address"]')
                    address = address_elem.get_text(strip=True) if address_elem else None
                    
                    hours_elem = location.select_one('.hours, [class*="hours"]')
                    hours = hours_elem.get_text(strip=True) if hours_elem else None
                    
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
                            open_hours=hours,
                            source_url=self.url
                        )
                        results.append(record)
                
                except Exception as e:
                    logger.error(f"Error parsing location: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error scraping City Harvest: {e}")
        
        return results
    
    def scrape_google_maps(self) -> List[Dict]:
        """Scrape Google My Maps"""
        results = []
        
        try:
            logger.info(f"Loading Google Maps with Selenium...")
            self.driver.get(self.url)
            
            # Wait for map to load
            time.sleep(8)
            
            # Try to expand the list view
            try:
                # Look for list/menu button
                menu_buttons = self.driver.find_elements(By.CSS_SELECTOR, '[aria-label*="menu"], [aria-label*="list"], button')
                for button in menu_buttons:
                    try:
                        button.click()
                        time.sleep(2)
                        break
                    except:
                        continue
            except:
                pass
            
            # Scroll to load more items
            for _ in range(5):
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)
            
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Google Maps uses specific classes for markers/locations
            locations = soup.select('[class*="place"], [class*="marker"], [class*="location"]')
            
            logger.info(f"Found {len(locations)} potential Google Maps locations")
            
            for location in locations:
                try:
                    # Extract name and address from Google Maps structure
                    text = location.get_text(strip=True)
                    
                    if len(text) > 10:  # Has some content
                        # Try to parse as name
                        lines = text.split('\n')
                        name = lines[0] if lines else None
                        address = lines[1] if len(lines) > 1 else None
                        
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
                    logger.error(f"Error parsing Google Maps location: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error scraping Google Maps: {e}")
        
        return results
    
    def scrape_arcgis_dashboard(self) -> List[Dict]:
        """Scrape ArcGIS dashboard with Selenium"""
        results = []
        
        try:
            logger.info(f"Loading ArcGIS dashboard with Selenium...")
            self.driver.get(self.url)
            
            # Wait for dashboard to load
            time.sleep(10)
            
            # Try to find data tables or lists
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Look for data in tables or lists
            tables = soup.select('table')
            
            for table in tables:
                rows = table.select('tr')
                for row in rows[1:]:  # Skip header
                    cells = row.select('td')
                    if len(cells) >= 2:
                        name = cells[0].get_text(strip=True)
                        address = cells[1].get_text(strip=True) if len(cells) > 1 else None
                        
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
            logger.error(f"Error scraping ArcGIS dashboard: {e}")
        
        return results
    
    def scrape_generic_js_site(self) -> List[Dict]:
        """Generic scraper for JavaScript sites"""
        results = []
        
        try:
            logger.info(f"Loading {self.url} with Selenium...")
            self.driver.get(self.url)
            
            # Wait for page to load
            time.sleep(8)
            
            # Scroll to trigger lazy loading
            for _ in range(5):
                self.driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(1)
            
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Special handling for One Love Community Fridge
            if 'onelovecommunityfridge.org' in self.url:
                # Find all h3 tags with links (fridge locations)
                fridge_headers = soup.select('h3 a[href*="maps"]')
                logger.info(f"Found {len(fridge_headers)} fridge locations")
                
                for header in fridge_headers:
                    try:
                        # Extract address from link text
                        address_text = header.get_text(strip=True)
                        # Clean up address (remove <br> tags)
                        address = address_text.replace('\n', ' ').strip()
                        
                        # Get neighborhood from previous sibling
                        parent = header.find_parent()
                        if parent:
                            prev_p = parent.find_previous_sibling('p')
                            neighborhood = prev_p.get_text(strip=True) if prev_p else None
                        else:
                            neighborhood = None
                        
                        # Get hosted by info
                        next_p = header.find_parent().find_next_sibling('p')
                        owner = next_p.get_text(strip=True) if next_p else None
                        if owner and 'Hosted by' in owner:
                            owner = owner.replace('Hosted by', '').strip()
                        
                        if address:
                            lat, lon = None, None
                            coords = self.geocoder.geocode(address)
                            if coords:
                                lat, lon = coords
                            
                            record = create_data_record(
                                name=f"{neighborhood} Community Fridge" if neighborhood else "Community Fridge",
                                address=address,
                                neighborhood=neighborhood,
                                lat=lat,
                                lon=lon,
                                data_type=self.data_type,
                                owner=owner,
                                source_url=self.url
                            )
                            results.append(record)
                    
                    except Exception as e:
                        logger.error(f"Error parsing fridge location: {e}")
                        continue
                
                return results
            
            # Generic scraping for other sites
            items = soup.select('article, .item, .location, .entry, .post, [class*="item"], [class*="location"]')
            
            logger.info(f"Found {len(items)} potential items")
            
            for item in items:
                try:
                    name = item.select_one('h1, h2, h3, h4, .title, .name')
                    name = name.get_text(strip=True) if name else None
                    
                    # Try to find address
                    address_elem = item.select_one('.address, [class*="address"]')
                    address = address_elem.get_text(strip=True) if address_elem else None
                    
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
                    logger.error(f"Error parsing item: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error in generic JS scraper: {e}")
        
        return results
