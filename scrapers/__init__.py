"""
Scrapers package
"""

from .base_scraper import BaseScraper
from .api_scraper import APIScraper
from .html_scraper import HTMLScraper
from .pdf_scraper import PDFScraper
from .map_scraper import MapScraper
from .selenium_scraper import SeleniumScraper

__all__ = ['BaseScraper', 'APIScraper', 'HTMLScraper', 'PDFScraper', 'MapScraper', 'SeleniumScraper']
