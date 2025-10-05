# NYC Food Access Data Scraper

A comprehensive Python-based web scraper for aggregating data about community gardens, farms, farmers markets, urban farms, community fridges, food banks/pantries, and CSA programs in the NYC metropolitan area.

## Geographic Coverage

- **NYC**: All 5 boroughs (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
- **Westchester County**
- **Yonkers**
- **Long Island** (Nassau and Suffolk Counties)
- **New Jersey**: 50 miles west from the Hudson River border

## Features

- **Multi-source scraping**: Handles APIs, HTML websites, and PDF documents
- **Automatic geocoding**: Converts addresses to latitude/longitude coordinates
- **Data normalization**: Standardizes phone numbers, addresses, and other fields
- **Deduplication**: Removes duplicate entries based on name and address
- **Geographic filtering**: Filters results to target area
- **Comprehensive logging**: Detailed logs for debugging and monitoring
- **Progress tracking**: Visual progress bars for long-running operations
- **Error handling**: Robust error handling with retry logic

## Data Sources

The scraper aggregates data from 30+ sources including:

### API Sources
- NYC Open Data (GreenThumb Gardens)

### HTML Sources
- NYC Parks GreenThumb
- LUNGS NYC
- Community Fridge Finder
- One Love Community Fridge
- Manhattan/Brooklyn-Queens/Bronx Land Trusts
- NYRP Gardens
- Food Bank NYC
- City Harvest
- GrowNYC Greenmarkets
- Local Harvest
- And many more...

### PDF Sources
- NYC DOH Farmers Markets Map
- NY Agriculture FMNP Schedule
- GrowNYC Market Map

See `config.py` for the complete list of data sources.

## Output Schema

Each record includes the following fields:

- `name`: Name of the location
- `address`: Street address
- `neighborhood`: Borough or neighborhood
- `lat`: Latitude coordinate
- `long`: Longitude coordinate
- `description`: Description of the location
- `type`: Type of location (community_garden, farm, farmers_market, urban_farm, community_fridge, food_bank, csa)
- `open_hours`: Operating hours
- `owner`: Owner or managing organization
- `local_items_selling`: Items available (for markets/farms)
- `contact_information`: Phone number or email
- `social_media_website1`: Primary website or social media
- `social_media_website2`: Secondary website or social media
- `source_url`: Original data source URL
- `last_updated`: Date of data collection

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Install Selenium WebDriver** (for JavaScript-heavy sites):
   ```bash
   # For Chrome
   # Download ChromeDriver from https://chromedriver.chromium.org/
   # Add to PATH or place in project directory
   ```

## Usage

### Basic Usage

Run the scraper to collect data from all configured sources:

```bash
python main.py
```

This will:
1. Scrape all configured data sources
2. Geocode addresses to coordinates
3. Clean and deduplicate the data
4. Filter by geographic bounds
5. Save results to a timestamped CSV file
6. Generate a summary report

### Output

The scraper generates:
- **CSV file**: `nyc_food_access_data_YYYYMMDD_HHMMSS.csv`
- **Log file**: `scraper_YYYYMMDD_HHMMSS.log`

### Customization

#### Adding New Data Sources

Edit `config.py` and add sources to the appropriate category:

```python
DATA_SOURCES = {
    "html_sources": [
        {
            "name": "My New Source",
            "url": "https://example.com/gardens",
            "type": "community_garden"
        }
    ]
}
```

#### Modifying Geographic Bounds

Edit the `GEOGRAPHIC_BOUNDS` in `config.py`:

```python
GEOGRAPHIC_BOUNDS = {
    "nyc_boroughs": ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"],
    "counties": ["Westchester County", "Nassau County", "Suffolk County"],
    # ... etc
}
```

#### Adjusting Rate Limiting

Edit `RATE_LIMIT` in `config.py`:

```python
RATE_LIMIT = {
    "requests_per_minute": 30,
    "delay_between_requests": 2  # seconds
}
```

## Architecture

```
├── main.py                 # Main orchestrator
├── config.py              # Configuration and data sources
├── utils.py               # Utility functions (geocoding, normalization)
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py    # Abstract base class
│   ├── api_scraper.py     # API/JSON scraper
│   ├── html_scraper.py    # HTML website scraper
│   └── pdf_scraper.py     # PDF document scraper
└── requirements.txt       # Python dependencies
```

## Scraper Types

### API Scraper
Handles structured API endpoints, especially:
- Socrata (NYC Open Data)
- Generic JSON APIs

### HTML Scraper
Scrapes HTML websites with custom logic for:
- NYC Parks
- Land trusts
- Food banks
- Farmers markets
- Community fridges

### PDF Scraper
Extracts data from PDF documents:
- Table extraction
- Text parsing with regex patterns
- Address and contact info extraction

## Dependencies

- **requests**: HTTP requests
- **beautifulsoup4**: HTML parsing
- **pandas**: Data manipulation and CSV export
- **lxml**: Fast HTML/XML parser
- **selenium**: Browser automation (for JavaScript sites)
- **PyPDF2**: PDF reading
- **pdfplumber**: Advanced PDF table extraction
- **geopy**: Geocoding addresses
- **tqdm**: Progress bars
- **python-dotenv**: Environment variable management
- **retry**: Retry logic for failed requests

## Troubleshooting

### Geocoding Rate Limits

If you encounter geocoding rate limits:
1. The scraper includes automatic retry logic with exponential backoff
2. Results are cached to avoid redundant geocoding
3. Consider using a paid geocoding service for large datasets

### Anti-Scraping Measures

Some sites have anti-scraping protections:
1. The scraper includes realistic User-Agent headers
2. Rate limiting is built-in (2 seconds between requests)
3. For problematic sites, consider using Selenium (slower but more reliable)

### Missing Data

If certain fields are missing:
1. Check the log file for errors
2. Inspect the source website's HTML structure
3. Update the CSS selectors in the appropriate scraper file
4. Some sources may not provide all fields

## Best Practices

1. **Run semi-annually**: Data changes slowly, so running every 6 months is sufficient
2. **Check logs**: Review log files for errors and warnings
3. **Verify coordinates**: Spot-check geocoded coordinates for accuracy
4. **Respect rate limits**: Don't modify rate limiting settings too aggressively
5. **Update sources**: Periodically check if source URLs have changed

## Legal and Ethical Considerations

- This scraper is designed for public data aggregation
- Always respect robots.txt and terms of service
- Use reasonable rate limiting to avoid overloading servers
- Some data sources may require attribution
- Verify data accuracy before use in production applications

## Future Enhancements

Potential improvements:
- [ ] Add support for Google Maps scraping
- [ ] Implement ArcGIS dashboard scraping
- [ ] Add web search for discovering new sources
- [ ] Create interactive map visualization
- [ ] Add data validation and quality checks
- [ ] Implement incremental updates (only scrape changed data)
- [ ] Add email notifications for scraping completion

## Contributing

To add support for new data sources:
1. Add the source to `config.py`
2. If needed, create custom parsing logic in the appropriate scraper
3. Test thoroughly with sample data
4. Update this README

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the log files for error messages
2. Review the source code comments
3. Verify your Python environment and dependencies
4. Ensure you have internet connectivity

## Acknowledgments

Data sources include:
- NYC Department of Parks and Recreation
- NYC Open Data
- GreenThumb
- Various land trusts and community organizations
- Food banks and pantries across NYC

Thank you to all organizations making food access data publicly available!
