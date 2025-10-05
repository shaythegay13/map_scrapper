"""
Main orchestrator for NYC Food Access Data Scraper
"""

import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict
from tqdm import tqdm
import sys

from config import DATA_SOURCES, OUTPUT_FIELDS
from scrapers import APIScraper, HTMLScraper, PDFScraper, MapScraper, SeleniumScraper
from utils import Geocoder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class DataAggregator:
    """Main class to orchestrate all scrapers"""
    
    def __init__(self):
        self.all_data = []
        self.geocoder = Geocoder()
    
    def run_all_scrapers(self):
        """Execute all configured scrapers"""
        
        logger.info("=" * 80)
        logger.info("Starting NYC Food Access Data Scraper")
        logger.info("=" * 80)
        
        # Scrape API sources
        logger.info("\n--- Scraping API Sources ---")
        for source in tqdm(DATA_SOURCES['api_sources'], desc="API Sources"):
            try:
                scraper = APIScraper(source)
                data = scraper.run()
                self.all_data.extend(data)
                logger.info(f"✓ {source['name']}: {len(data)} records")
            except Exception as e:
                logger.error(f"✗ {source['name']}: {e}")
        
        # Scrape HTML sources
        logger.info("\n--- Scraping HTML Sources ---")
        for source in tqdm(DATA_SOURCES['html_sources'], desc="HTML Sources"):
            try:
                # Use Selenium for JavaScript-heavy sites
                if source.get('use_selenium', False):
                    logger.info(f"Using Selenium for: {source['name']}")
                    scraper = SeleniumScraper(source)
                else:
                    scraper = HTMLScraper(source)
                
                data = scraper.run()
                self.all_data.extend(data)
                logger.info(f"✓ {source['name']}: {len(data)} records")
            except Exception as e:
                logger.error(f"✗ {source['name']}: {e}")
        
        # Scrape PDF sources
        logger.info("\n--- Scraping PDF Sources ---")
        for source in tqdm(DATA_SOURCES['pdf_sources'], desc="PDF Sources"):
            try:
                scraper = PDFScraper(source)
                data = scraper.run()
                self.all_data.extend(data)
                logger.info(f"✓ {source['name']}: {len(data)} records")
            except Exception as e:
                logger.error(f"✗ {source['name']}: {e}")
        
        # Scrape Map sources
        if 'map_sources' in DATA_SOURCES and DATA_SOURCES['map_sources']:
            logger.info("\n--- Scraping Map Sources ---")
            for source in tqdm(DATA_SOURCES['map_sources'], desc="Map Sources"):
                try:
                    # Use Selenium for Google Maps
                    if 'google.com/maps' in source['url']:
                        logger.info(f"Using Selenium for Google Maps: {source['name']}")
                        scraper = SeleniumScraper(source)
                    else:
                        scraper = MapScraper(source)
                    
                    data = scraper.run()
                    self.all_data.extend(data)
                    logger.info(f"✓ {source['name']}: {len(data)} records")
                except Exception as e:
                    logger.error(f"✗ {source['name']}: {e}")
        
        # Note: Image sources and data portal sources require manual handling
        if 'image_sources' in DATA_SOURCES and DATA_SOURCES['image_sources']:
            logger.info("\n--- Image Sources (Manual Extraction Required) ---")
            for source in DATA_SOURCES['image_sources']:
                logger.info(f"⚠ {source['name']}: {source['note']}")
        
        if 'data_portal_sources' in DATA_SOURCES and DATA_SOURCES['data_portal_sources']:
            logger.info("\n--- Data Portal Sources (Using API Instead) ---")
            for source in DATA_SOURCES['data_portal_sources']:
                logger.info(f"ℹ {source['name']}: {source['note']}")
        
        logger.info("\n" + "=" * 80)
        logger.info(f"Total records collected: {len(self.all_data)}")
        logger.info("=" * 80)
    
    def clean_and_deduplicate(self):
        """Clean data and remove duplicates"""
        
        logger.info("\n--- Cleaning and Deduplicating Data ---")
        
        initial_count = len(self.all_data)
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(self.all_data)
        
        # Only remove records that have BOTH name AND address missing
        # Keep records with at least one of these fields
        before_filter = len(df)
        df = df[df['name'].notna() | df['address'].notna()]
        removed = before_filter - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} records with no name AND no address")
        else:
            logger.info(f"All records have at least a name or address - keeping all {len(df)} records")
        
        # Remove duplicates only if BOTH name and address match exactly
        # This handles true duplicates while keeping similar entries
        before_dedup = len(df)
        
        # Create a composite key for deduplication
        # Only consider it a duplicate if both name and address are identical
        df['_dedup_key'] = df.apply(
            lambda row: f"{str(row.get('name', '')).lower().strip()}|||{str(row.get('address', '')).lower().strip()}", 
            axis=1
        )
        df = df.drop_duplicates(subset=['_dedup_key'], keep='first')
        df = df.drop(columns=['_dedup_key'])
        
        logger.info(f"Removed {before_dedup - len(df)} exact duplicate records")
        
        # Filter by geographic bounds if coordinates exist
        if 'lat' in df.columns and 'long' in df.columns:
            before_filter = len(df)
            df = df[df.apply(lambda row: self.is_in_bounds(row), axis=1)]
            logger.info(f"Removed {before_filter - len(df)} records outside geographic bounds")
        
        # Sort by type and name
        df = df.sort_values(['type', 'name'], na_position='last')
        
        # Ensure all output fields are present
        for field in OUTPUT_FIELDS:
            if field not in df.columns:
                df[field] = None
        
        # Reorder columns
        df = df[OUTPUT_FIELDS]
        
        self.all_data = df.to_dict('records')
        
        logger.info(f"Final record count: {len(self.all_data)}")
    
    def is_in_bounds(self, row) -> bool:
        """Check if a record is within geographic bounds"""
        try:
            lat = row.get('lat')
            lon = row.get('long')
            
            if pd.isna(lat) or pd.isna(lon):
                return True  # Keep records without coordinates
            
            return self.geocoder.is_within_bounds(float(lat), float(lon))
        except:
            return True
    
    def save_to_csv(self, filename: str = None):
        """Save data to CSV file"""
        
        if filename is None:
            filename = f"nyc_food_access_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            df = pd.DataFrame(self.all_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"\n✓ Data saved to: {filename}")
            
            # Print summary statistics
            logger.info("\n--- Summary Statistics ---")
            if 'type' in df.columns:
                type_counts = df['type'].value_counts()
                for data_type, count in type_counts.items():
                    logger.info(f"  {data_type}: {count}")
            
            return filename
        
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return None
    
    def generate_report(self):
        """Generate a summary report"""
        
        logger.info("\n" + "=" * 80)
        logger.info("SCRAPING REPORT")
        logger.info("=" * 80)
        
        df = pd.DataFrame(self.all_data)
        
        logger.info(f"\nTotal Records: {len(df)}")
        
        if 'type' in df.columns:
            logger.info("\nRecords by Type:")
            for data_type, count in df['type'].value_counts().items():
                logger.info(f"  - {data_type}: {count}")
        
        # Count records with coordinates
        if 'lat' in df.columns and 'long' in df.columns:
            geocoded = df[df['lat'].notna() & df['long'].notna()]
            logger.info(f"\nGeocoded Records: {len(geocoded)} ({len(geocoded)/len(df)*100:.1f}%)")
        
        # Count records with contact info
        if 'contact_information' in df.columns:
            with_contact = df[df['contact_information'].notna()]
            logger.info(f"Records with Contact Info: {len(with_contact)} ({len(with_contact)/len(df)*100:.1f}%)")
        
        # Count records with hours
        if 'open_hours' in df.columns:
            with_hours = df[df['open_hours'].notna()]
            logger.info(f"Records with Hours: {len(with_hours)} ({len(with_hours)/len(df)*100:.1f}%)")
        
        logger.info("\n" + "=" * 80)


def main():
    """Main execution function"""
    
    try:
        # Create aggregator
        aggregator = DataAggregator()
        
        # Run all scrapers
        aggregator.run_all_scrapers()
        
        # Clean and deduplicate
        aggregator.clean_and_deduplicate()
        
        # Save to CSV
        output_file = aggregator.save_to_csv()
        
        # Generate report
        aggregator.generate_report()
        
        logger.info("\n✓ Scraping completed successfully!")
        
        if output_file:
            logger.info(f"\nOutput file: {output_file}")
        
    except KeyboardInterrupt:
        logger.info("\n\nScraping interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"\n\nFatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
