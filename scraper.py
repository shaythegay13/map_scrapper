"""
DEPRECATED: This file has been replaced by the modular scraper system.
Please use main.py instead.

For the NYC Food Access Data Scraper, run:
    python main.py

This will scrape all configured sources and output a consolidated CSV file.
"""

import sys

def main():
    print("=" * 80)
    print("DEPRECATED: This scraper has been replaced")
    print("=" * 80)
    print("\nPlease use the new modular scraper system:")
    print("  python main.py")
    print("\nThe new system includes:")
    print("  - Multi-source scraping (APIs, HTML, PDFs)")
    print("  - Automatic geocoding")
    print("  - Data deduplication")
    print("  - Geographic filtering")
    print("  - Comprehensive logging")
    print("=" * 80)
    sys.exit(0)

if __name__ == "__main__":
    main()
