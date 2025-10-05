# Selenium Setup Guide

## What is Selenium?

Selenium allows the scraper to interact with JavaScript-heavy websites that load data dynamically. This is essential for sites like:
- NYC Food Help Finder (interactive map)
- City Harvest Food Map (JavaScript-based)
- Google My Maps (dynamic content)
- ArcGIS Dashboards (interactive dashboards)

## Installation Status

✅ **ChromeDriver installed**: Version 114.0.5735.90

## Which Sources Use Selenium?

The following sources are configured to use Selenium:

### HTML Sources:
- **NYC Food Help Finder** - Interactive food assistance map
- **City Harvest Food Map** - Dynamic food bank locations

### Map Sources:
- **All Google My Maps** - Community fridges and farmers markets maps

## Running the Scraper with Selenium

Simply run the main scraper - it will automatically use Selenium for marked sources:

```bash
./venv/bin/python main.py
```

The scraper will:
1. Use regular HTTP requests for static sites (fast)
2. Launch headless Chrome for JavaScript sites (slower but thorough)
3. Automatically switch between methods based on source configuration

## Performance Notes

- **Selenium sources are slower**: Each takes 10-30 seconds vs 2-5 seconds for regular HTTP
- **Headless mode**: Chrome runs in background (no visible window)
- **Memory usage**: Each Selenium session uses ~200MB RAM
- **Total time**: Expect 15-25 minutes for full scrape with Selenium enabled

## Troubleshooting

### ChromeDriver Version Mismatch
If you see errors about ChromeDriver version:
```bash
./setup_selenium.sh
```

### Chrome Not Found
Install Chromium:
```bash
sudo apt-get install chromium-browser
```

### Selenium Timeout Errors
Increase wait times in `scrapers/selenium_scraper.py`:
```python
time.sleep(10)  # Increase from 5 to 10 seconds
```

### Memory Issues
If running out of memory, disable Selenium for some sources by removing `"use_selenium": True` from `config.py`

## Adding More Selenium Sources

To mark a source for Selenium scraping, add to `config.py`:

```python
{
    "name": "My JavaScript Site",
    "url": "https://example.com",
    "type": "farmers_market",
    "use_selenium": True  # Add this flag
}
```

## Customizing Selenium Behavior

Edit `scrapers/selenium_scraper.py` to:
- Adjust wait times
- Add custom click/scroll actions
- Modify element selectors
- Add screenshot capture for debugging

## Benefits of Selenium

✅ Access JavaScript-rendered content
✅ Interact with dynamic maps and widgets
✅ Handle infinite scroll and lazy loading
✅ Bypass some anti-scraping measures
✅ Capture data from interactive dashboards

## Limitations

❌ Slower than regular HTTP requests
❌ Higher memory usage
❌ May still be blocked by advanced anti-bot systems
❌ Requires Chrome/Chromium installed
❌ More complex to debug
