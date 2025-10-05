"""
Scraper for PDF documents
"""

import io
import re
import logging
from typing import List, Dict
import pdfplumber
from .base_scraper import BaseScraper
from utils import create_data_record, Geocoder

logger = logging.getLogger(__name__)


class PDFScraper(BaseScraper):
    """Scraper for PDF documents"""
    
    def __init__(self, source_config: Dict):
        super().__init__(source_config)
        self.geocoder = Geocoder()
    
    def scrape(self) -> List[Dict]:
        """Scrape data from PDF"""
        results = []
        
        try:
            # Download PDF
            response = self.get_page(self.url)
            if not response:
                return results
            
            # Parse PDF
            pdf_file = io.BytesIO(response.content)
            
            with pdfplumber.open(pdf_file) as pdf:
                logger.info(f"Processing PDF with {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    logger.info(f"Processing page {page_num}/{len(pdf.pages)}")
                    
                    # Extract text
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    # Try to extract tables first
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            records = self.parse_table(table)
                            results.extend(records)
                    
                    # Also parse text for additional info
                    text_records = self.parse_text(text)
                    results.extend(text_records)
        
        except Exception as e:
            logger.error(f"Error scraping PDF {self.url}: {e}")
        
        return results
    
    def parse_table(self, table: List[List[str]]) -> List[Dict]:
        """
        Parse a table from PDF
        
        Args:
            table: 2D list of table cells
            
        Returns:
            List of data records
        """
        results = []
        
        if not table or len(table) < 2:
            return results
        
        # Assume first row is header
        headers = [str(h).lower().strip() if h else '' for h in table[0]]
        
        # Find relevant column indices
        name_idx = self.find_column_index(headers, ['name', 'market', 'location', 'site', 'garden'])
        address_idx = self.find_column_index(headers, ['address', 'location', 'street'])
        hours_idx = self.find_column_index(headers, ['hours', 'time', 'schedule', 'days', 'when'])
        phone_idx = self.find_column_index(headers, ['phone', 'contact', 'tel'])
        
        # Process data rows
        for row in table[1:]:
            if not row or all(not cell for cell in row):
                continue
            
            try:
                name = row[name_idx] if name_idx is not None and name_idx < len(row) else None
                address = row[address_idx] if address_idx is not None and address_idx < len(row) else None
                hours = row[hours_idx] if hours_idx is not None and hours_idx < len(row) else None
                phone = row[phone_idx] if phone_idx is not None and phone_idx < len(row) else None
                
                # Clean up values
                name = str(name).strip() if name else None
                address = str(address).strip() if address else None
                hours = str(hours).strip() if hours else None
                phone = str(phone).strip() if phone else None
                
                if name or address:
                    # Geocode
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
                        contact=phone,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing table row: {e}")
                continue
        
        return results
    
    def parse_text(self, text: str) -> List[Dict]:
        """
        Parse unstructured text from PDF
        
        Args:
            text: Extracted text from PDF page
            
        Returns:
            List of data records
        """
        results = []
        
        # Split into potential entries (by double newline or specific patterns)
        entries = re.split(r'\n\s*\n', text)
        
        for entry in entries:
            if len(entry.strip()) < 20:  # Skip very short entries
                continue
            
            try:
                # Look for name (usually first line or bold/caps)
                lines = entry.strip().split('\n')
                name = lines[0].strip() if lines else None
                
                # Look for address pattern
                address_match = re.search(
                    r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Place|Pl)[,\s]+(?:Brooklyn|Manhattan|Queens|Bronx|Staten Island|NY)',
                    entry,
                    re.IGNORECASE
                )
                address = address_match.group() if address_match else None
                
                # Look for phone number
                phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', entry)
                phone = phone_match.group() if phone_match else None
                
                # Look for hours/days
                hours_match = re.search(
                    r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Mon|Tue|Wed|Thu|Fri|Sat|Sun)[\w\s,:-]+(?:\d{1,2}:\d{2}|am|pm)',
                    entry,
                    re.IGNORECASE
                )
                hours = hours_match.group() if hours_match else None
                
                if name and (address or phone):
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
                        contact=phone,
                        source_url=self.url
                    )
                    results.append(record)
            
            except Exception as e:
                logger.error(f"Error parsing text entry: {e}")
                continue
        
        return results
    
    @staticmethod
    def find_column_index(headers: List[str], keywords: List[str]) -> int:
        """
        Find column index by matching keywords
        
        Args:
            headers: List of column headers
            keywords: List of keywords to match
            
        Returns:
            Column index or None if not found
        """
        for i, header in enumerate(headers):
            for keyword in keywords:
                if keyword in header:
                    return i
        return None
