# Debugging Notes - Food Banks & Selenium Issues

## Problems Identified

### 1. ❌ No Food Banks/Pantries in Results
**Issue**: 0 food bank/pantry records despite having sources configured
**Root Causes**:
- Selenium sources failed due to ChromeDriver version mismatch
- HTML food bank sites use complex JavaScript
- No API sources for food banks/pantries

### 2. ❌ Selenium ChromeDriver Version Mismatch
**Issue**: ChromeDriver 114 vs Chrome 141
**Error**: `This version of ChromeDriver only supports Chrome version 114`
**Impact**: All Selenium scrapers returned 0 records

## Fixes Applied

### ✅ Fix 1: Updated ChromeDriver
```bash
# Downloaded ChromeDriver 141.0.7390.54 to match Chrome 141
wget https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.54/linux64/chromedriver-linux64.zip
sudo mv chromedriver /usr/local/bin/
```

**Status**: ✅ ChromeDriver now matches Chrome version

### ✅ Fix 2: Added Food Resource API Sources
Added to `config.py`:
- NYC Open Data - Food Scrap Drop Off Locations
- NYC Open Data - FRESH Food Stores

**Status**: ✅ Now scraping 3 API sources instead of 1

### 🔄 Fix 3: Selenium Scraper Improvements (In Progress)
The Selenium scrapers need better selectors for:
- NYC Food Help Finder
- City Harvest Food Map
- Google My Maps

**Current Status**: ChromeDriver fixed, but selectors still need work

## Current Scraper Run

**Process**: Running with fixed ChromeDriver + new food APIs
**Expected**: More food-related records
**Log File**: `scraper_run_fixed.log`

## Why Food Banks Are Hard to Scrape

### Challenge 1: Interactive Maps
Sites like NYC Food Help Finder use:
- Complex JavaScript frameworks (React/Angular)
- Dynamic loading (AJAX requests)
- Interactive map widgets
- Anti-scraping measures

### Challenge 2: No Public APIs
Unlike GreenThumb gardens, most food banks don't have:
- Public REST APIs
- Structured data exports
- Machine-readable formats

### Challenge 3: Data Fragmentation
Food bank data is spread across:
- Individual organization websites
- City/state databases
- Non-profit directories
- Google Maps listings

## Alternative Approaches for Food Banks

### Option 1: Manual Data Collection
- Visit key sites manually
- Copy data to spreadsheet
- Import to CSV

### Option 2: Use Existing Datasets
- NYC Open Data portal
- USDA Food Access Research Atlas
- Feeding America locator data
- 211 service databases

### Option 3: API Partnerships
- Contact organizations directly
- Request data exports
- Partner with data aggregators

## Selenium Debugging Tips

### Test Individual Sites
```python
from scrapers.selenium_scraper import SeleniumScraper

source = {"name": "Test", "url": "https://example.com", "type": "food_bank"}
scraper = SeleniumScraper(source)
results = scraper.run()
```

### Add Screenshots for Debugging
In `selenium_scraper.py`:
```python
self.driver.save_screenshot('debug.png')
```

### Increase Wait Times
```python
time.sleep(10)  # Instead of 5
```

### Inspect Page Source
```python
with open('page_source.html', 'w') as f:
    f.write(self.driver.page_source)
```

## Next Steps

### Immediate (Current Run)
- ✅ ChromeDriver updated
- ✅ Food resource APIs added
- 🔄 Scraper running now

### Short Term
- Debug Selenium selectors for each site
- Add more NYC Open Data food sources
- Test with screenshots

### Long Term
- Partner with food access organizations
- Build database of manually verified locations
- Create web form for community submissions

## Expected Results from Current Run

With the fixes:
- **Community Gardens**: ~624 (same)
- **Farmers Markets**: ~51 (same)
- **Urban Farms**: ~6 (same)
- **Food Resources**: NEW - from added APIs
- **Total**: 700+ records (estimate)

**Note**: Food banks/pantries may still be 0 until Selenium selectors are fixed, but we'll have more food-related resources from the new APIs.
