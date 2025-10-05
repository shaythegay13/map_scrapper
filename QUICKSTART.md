# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Run the Scraper

```bash
python main.py
```

That's it! The scraper will:
1. Collect data from 30+ sources
2. Geocode all addresses
3. Clean and deduplicate
4. Save to CSV with timestamp

## Output Files

- `nyc_food_access_data_YYYYMMDD_HHMMSS.csv` - Your data
- `scraper_YYYYMMDD_HHMMSS.log` - Detailed logs

## What Gets Scraped

- **Community Gardens**: 500+ gardens across NYC
- **Farmers Markets**: 100+ markets
- **Urban Farms**: 50+ farms
- **Community Fridges**: 50+ locations
- **Food Banks/Pantries**: 200+ locations
- **CSA Programs**: Various programs

## Expected Runtime

- **First run**: 30-60 minutes (includes geocoding)
- **Subsequent runs**: 20-40 minutes (cached geocoding)

## Common Issues

### Rate Limiting
If you see "Too many requests" errors:
- The scraper automatically retries with backoff
- Wait a few minutes and restart if needed

### Missing Data
Some sources may not provide all fields:
- Check the log file for specific errors
- Not all sources have phone numbers, hours, etc.

### Geocoding Failures
If addresses can't be geocoded:
- They'll still be included in the output
- Lat/long fields will be empty
- Consider manual geocoding for important entries

## Next Steps

1. **Review the CSV**: Check data quality
2. **Filter by type**: Use `type` column to filter
3. **Map the data**: Import CSV into mapping software
4. **Update sources**: Add new sources to `config.py`

## Tips

- Run semi-annually to keep data fresh
- Back up previous CSV files before running
- Check logs for any errors or warnings
- Verify a sample of geocoded coordinates

## Need Help?

See the full README.md for detailed documentation.
