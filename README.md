# NYC Food Access Scraper

This is Shay Bouchles's scraper for [Saved by the Plate](https://savedbytheplate.org), a nonprofit project that maps places where people can grow, buy, or pick up food. It collects public listings for community gardens, farmers markets, farms, urban farms, community fridges, food banks and pantries, CSAs, and FRESH food stores so they can live on one map.

As of 14 October 2026, `https://savedbytheplate.org` returns HTTP 404 and does not serve that map. This repository is the collection pipeline, plus CSV snapshots from the October 2025 collection.

The older write-ups in this repo (`PROJECT_SUMMARY.md`, `FINAL_SUMMARY.md`, `QUICKSTART.md` as it used to read, `SCRAPER_STATUS.md`, and the debugging notes) describe that collection while it was in progress. Their source counts and record counts do not all match `config.py` or the CSV files as they are now. This README was checked against the code.

## Location types

Each record's `type` comes from the source entry in `config.py`. These are the values the code assigns:

| `type` | What it means in this project |
| --- | --- |
| `community_garden` | Community gardens and land-trust garden lists |
| `farmers_market` | Farmers markets and greenmarkets |
| `farm` | Farm stands and farms that are not tagged as urban farms |
| `urban_farm` | Urban farms, rooftop farms, and teaching farms |
| `community_fridge` | Community fridges |
| `food_bank` | Food banks, pantries, and the NYC Food Help Finder |
| `csa` | CSA programs |
| `food_store` | NYC FRESH food stores (Open Data API only) |

`config.py` also names a target area: the five NYC boroughs, Westchester County, Yonkers, Nassau and Suffolk Counties, and New Jersey within about 50 miles of a point in New York City. The filter that actually runs is simpler. After scraping, rows that already have coordinates are kept only when latitude is between 40.0 and 41.5 and longitude is between -74.8 and -71.8. Rows with no coordinates are kept. The borough list and the 50-mile figure are not applied.

## Data sources

`config.py` lists **51 entries**. `main.py` fetches the API, HTML, PDF, and map groups. It only logs the image entry and the two NYC Open Data portal pages.

Parsers below are what the code calls. A "page-specific" parser means a function with its own selectors. Those selectors were written against the sites as they looked when the scraper was built. This documentation pass did not re-fetch the sites, so a parser existing is not a claim that it still returns records.

### Open data APIs

`APIScraper` pages through Socrata (`$limit` 1000) and maps GreenThumb fields (garden name, borough code, per-day hours, jurisdiction) when those keys are present.

| Source | Type | URL |
| --- | --- | --- |
| NYC Open Data — GreenThumb Gardens | `community_garden` | https://data.cityofnewyork.us/resource/p78i-pat6.json |
| NYC Open Data — FRESH Food Stores | `food_store` | https://data.cityofnewyork.us/resource/3ayg-qpzm.json |

### HTML with a page-specific parser

`HTMLScraper` downloads the page with `requests` and BeautifulSoup (`lxml`).

| Source | Type | URL |
| --- | --- | --- |
| NYC Parks GreenThumb | `community_garden` | https://www.nycgovparks.org/greenthumb/community-gardens |
| LUNGS NYC Gardens & Greenspaces | `community_garden` | https://lungsnyc.org/gardens-greenspaces/ |
| Community Fridge Finder | `community_fridge` | https://www.communityfridgefinder.com/browse |
| Manhattan Land Trust | `community_garden` | https://www.manhattanlandtrust.org/our-gardens/ |
| Brooklyn Queens Land Trust | `community_garden` | https://bqlt.org/our-gardens and https://bqlt.org/ |
| Bronx Land Trust | `community_garden` | https://www.bronxlandtrust.org/ourgardens and https://www.bronxlandtrust.org/ |
| NYRP Gardens and Parks | `community_garden` | https://www.nyrp.org/en/gardens-and-parks/ |
| Food Bank For New York City | `food_bank` | https://www.foodbanknyc.org/get-help/ |
| GrowNYC Greenmarket | `farmers_market` | https://www.grownyc.org/greenmarket/ourmarkets |
| Local Harvest markets | `farmers_market` | https://www.localharvest.org/search.jsp?map=1&lat=40.75&lon=-73.99&scale=11&ty=1 |
| Local Harvest CSAs | `csa` | https://www.localharvest.org/search.jsp?map=1&lat=40.75&lon=-73.99&scale=11&ty=6 |

Local Harvest is the HTML parser with selectors tied to that site's markup (`div.membercell`). The others try a handful of generic class names and address regular expressions. Community Fridge Finder is called out in config as a map that is hard to scrape.

### HTML with generic selectors

These 22 pages use `HTMLScraper.scrape_generic()`, which keeps `article`, `.location`, `.item`, `.entry`, and `.post` blocks that contain a heading or a street-like string.

| Source | Type | URL |
| --- | --- | --- |
| Freedge | `community_fridge` | https://www.freedge.org/locations |
| NYC Mutual Aid Network | `community_fridge` | https://mutualaid.nyc/resources/ |
| Bed-Stuy Strong | `community_fridge` | https://www.bedstuystrong.com/community-fridge |
| NY Alternative Land Trust | `community_garden` | https://www.nyalt.org/ |
| Zachary Schulman Garden Leaders | `community_garden` | https://zacharyschulman.com/gardenleaders |
| Project Evergreen | `community_garden` | https://projectevergreen.org/greencare-for-communities/ |
| EHR90Z Wix site | `community_garden` | https://ehr90z.wixsite.com/my-site-2/projects-3 |
| Secret NYC | `farmers_market` | https://secretnyc.co/farmers-markets-nyc/ |
| NYC Tourism | `farmers_market` | https://www.nyctourism.com/articles/best-farmers-markets-new-york-city/ |
| Just Food value-chain map | `farmers_market` | https://www.justfood.org/value-chain-map?tags=community-%20run%20farmers%20market%20site |
| Public Markets NYC | `farmers_market` | https://publicmarkets.nyc/jamaica-farmers-market |
| South Bronx Farmers Market | `farmers_market` | http://southbronxfarmersmarket.com/ |
| NY Agriculture farmers markets | `farmers_market` | https://agriculture.ny.gov/farmersmarkets |
| UB Healthy Project | `farmers_market` | https://ubhealthyproject.org/farmersmarket/ |
| Queens Farm farmstand | `farm` | https://www.queensfarm.org/farmstand/ |
| Wellspring Forest Farm | `farm` | https://www.wellspringforestfarm.com/ |
| Farming with Trees | `farm` | https://www.farmingwithtrees.org/home |
| Sprout Up | `urban_farm` | https://www.sproutup.org/exploring-a-farm |
| Garden Kitchen Lab | `urban_farm` | https://gardenkitchenlab.org/our-farms/ |
| NYBG Edible Academy | `urban_farm` | https://www.nybg.org/education/childrens-education/edible-academy/ |
| Bonton Farms | `urban_farm` | https://bontonfarms.org/ |
| The Last Farm in NYC | `csa` | https://thelastfarminnewyorkcity.com/markets-csas/ |

Some of these organizations are outside the NYC area (Bonton Farms is in Dallas). If geocoding returns coordinates outside the box above, the row is dropped. If geocoding fails, the row is kept with empty coordinates.

### Headless Chrome

`SeleniumScraper` starts Chrome in headless mode. `main.py` uses it for HTML sources with `use_selenium: True`, and for map URLs on `google.com/maps`.

| Source | Type | URL | What the code looks for |
| --- | --- | --- | --- |
| One Love Community Fridge — fridges | `community_fridge` | https://www.onelovecommunityfridge.org/fridges | `h3` links whose href contains `maps` |
| One Love Community Fridge — home | `community_fridge` | https://www.onelovecommunityfridge.org/ | Same One Love parser |
| NYC Food Help Finder | `food_bank` | https://finder.nyc.gov/foodhelp/locations?mView=map | `li[data-locationid]` after clicking `#load-all-btn` |
| City Harvest food map | `food_bank` | https://www.cityharvest.org/food-map/ | `.location`, `.pantry`, `.site`, `article`, and classes containing `location` |
| Community Fridge Google My Map | `community_fridge` | https://www.google.com/maps/d/u/0/viewer?mid=1c4jHrGl0ymGUXPDUPXCTmKdMD00FgJzl&ll=40.69109846326807%2C-73.97261285000002&z=13 | Elements whose class contains `place`, `marker`, or `location` |
| Farmers Markets Google My Map | `farmers_market` | https://www.google.com/maps/d/u/0/viewer?mid=1fqTOVOwP6fj4NXOpFHT2Y48e3zEghRiJ&ll=40.760619747874344%2C-73.98352704302141&z=11 | Same Google Maps parser |
| Farmers Markets Google My Map (same map id, different center) | `farmers_market` | https://www.google.com/maps/d/u/0/viewer?mid=1fqTOVOwP6fj4NXOpFHT2Y48e3zEghRiJ&ll=40.76009965033155%2C-73.83795819536516&z=11 | Same Google Maps parser |

### PDFs

`PDFScraper` downloads the file and reads it with `pdfplumber`. It keeps table rows whose header matches name, address, hours, or phone keywords, and it also splits page text on blank lines and looks for a street address or a phone number.

| Source | Type | URL |
| --- | --- | --- |
| NYC Health farmers-market map | `farmers_market` | https://www.nyc.gov/assets/doh/downloads/pdf/cdp/farmers-markets-map.pdf |
| NY Agriculture FMNP schedule | `farmers_market` | https://agriculture.ny.gov/system/files/documents/2025/06/fmnpmarketschedulescountiesnyc.pdf |
| GrowNYC market map | `farmers_market` | https://www.grownyc.org/files/gmkt/map.pdf |

### Maps other than Google My Maps

The NYC ArcGIS dashboard is handled by `MapScraper`, not by opening the dashboard. The scraper tries these FeatureServer query URLs and stops at the first one that returns features:

- `.../GreenThumb_Garden_Info/FeatureServer/0/query`
- `.../Urban_Agriculture/FeatureServer/0/query`
- `.../Food_Access/FeatureServer/0/query`

The host is `services5.arcgis.com/GfwWNkhOj9bNBqoJ`. The dashboard URL itself is only stored as `source_url`: https://nyc.maps.arcgis.com/apps/dashboards/7d3e668dfcdd4bce93275dae44fcd3dd

`MapScraper` also has a Google My Maps branch that fetches a KML URL and then logs that KML parsing is not implemented. `main.py` does not use that branch. Google My Maps entries go to Selenium instead.

### Listed, not fetched

| Source | Type | URL | What `main.py` does |
| --- | --- | --- | --- |
| Project Evergreen NYC map image | `community_garden` | https://projectevergreen.org/wp-content/uploads/2025/03/PE-NYC-Map-2025_001.jpg | Logs that extraction would be manual or OCR |
| GreenThumb about-data page | `community_garden` | https://data.cityofnewyork.us/dataset/GreenThumb-Garden-Info/p78i-pat6/about_data | Logs that the API should be used instead |
| GreenThumb data-preview page | `community_garden` | https://data.cityofnewyork.us/dataset/GreenThumb-Garden-Info/p78i-pat6/data_preview | Logs that the API should be used instead |

`ocr_lungs_map.py` is a separate script. It downloads a 2017 LUNGS map JPEG (`lungsnyc.org`), runs Tesseract, and writes `lungs_map_gardens.csv`. It is not called from `main.py`, and its packages are not in `requirements.txt`. `config.py`'s image entry is a different file (a Project Evergreen JPG).

## How a run works

`python main.py` builds a `DataAggregator` and does the following.

1. Walks `DATA_SOURCES['api_sources']`, then `html_sources`, then `pdf_sources`, then `map_sources`. One failed source is logged and skipped. The image and data-portal groups are log lines only.
2. Each scraper returns dictionaries from `create_data_record()` in `utils.py`. That helper expands street abbreviations (`St` to `Street`, and the same idea for Ave, Rd, Blvd, Dr, Ln, Pl, Ct), reformats 10-digit phone numbers, copies a borough name out of the address when the neighborhood is empty, and sets `last_updated` to today's date.
3. Coordinates are filled inside the scrapers, not in a later pass in `main.py`. Socrata records use latitude and longitude fields when the API sends them (including `the_geom`). Otherwise, if there is an address and no coordinates, `Geocoder` calls OpenStreetMap Nominatim. The geocoder appends `, New York` to the address. Results are cached on the `Geocoder` instance for that process only. The cache is not written to disk.
4. Drops rows where both `name` and `address` are empty.
5. Drops a later row when both the lowercased name and the lowercased address match an earlier row. Similar names with different addresses both stay.
6. Drops rows whose coordinates fall outside the box described above. Rows without coordinates stay.
7. Sorts by `type`, then `name`, and writes only the columns in `OUTPUT_FIELDS`.
8. Writes `nyc_food_access_data_YYYYMMDD_HHMMSS.csv` and prints counts by type, plus how many rows have coordinates, a contact, and hours. A log file `scraper_YYYYMMDD_HHMMSS.log` is created at startup.

`scraper.py` is a stub. Running it prints that it is deprecated and exits. Use `main.py`.

`config_old.py` is an earlier source list. Nothing imports it.

```
main.py                         # runs every configured source, then cleans and writes CSV
config.py                       # 51 source entries, output columns, unused rate-limit settings
utils.py                        # address and phone cleanup, Nominatim geocoding
scrapers/base_scraper.py        # requests session, 2-second pause after a successful fetch
scrapers/api_scraper.py         # Socrata and generic JSON
scrapers/html_scraper.py        # requests + BeautifulSoup
scrapers/pdf_scraper.py         # pdfplumber
scrapers/map_scraper.py         # guessed ArcGIS endpoints; KML path is unfinished
scrapers/selenium_scraper.py    # headless Chrome
merge_manual_data.py            # appends manual_data/community_fridges.csv
clean_csv.py                    # drops rows that look like broken PDF text
ocr_lungs_map.py                # optional, not part of a normal run
manual_data/                    # hand-entered fridges and urban farms
```

## Output format

CSV, UTF-8, no index column. Empty fields are blank. These columns are always present on a file written by `main.py`, in this order:

| Column | Contents |
| --- | --- |
| `name` | Place or program name |
| `address` | Street address, sometimes only a city |
| `neighborhood` | Borough, neighborhood, or community board when the scraper found one |
| `lat` | Latitude, or empty |
| `long` | Longitude, or empty |
| `description` | Notes, cross streets, or a short blurb |
| `type` | One of the type values above |
| `open_hours` | Hours text, or empty |
| `owner` | Operator, host, or jurisdiction |
| `local_items_selling` | Always empty. `create_data_record()` accepts it, and no scraper passes a value |
| `contact_information` | Phone, or sometimes an email |
| `social_media_website1` | A site or profile when that scraper stored one |
| `social_media_website2` | Always empty. `DataNormalizer.extract_social_media()` can return a second URL, and nothing calls it |
| `source_url` | Page, API, PDF, or map the row came from. Manual rows use `Manual Entry` |
| `last_updated` | `YYYY-MM-DD` when the row was built |

### Files already in the repo

These are snapshots from the October 2025 collection, not a fresh scrape. Line counts in an editor are higher than the record counts because some cells contain line breaks. Counts below are parsed records.

| File | Records | Notes |
| --- | --- | --- |
| `nyc_food_access_data_COMPLETE.csv` | 1,279 | 626 community gardens, 511 food banks, 63 farmers markets, 41 urban farms, 25 community fridges, 13 CSAs. No `farm` or `food_store` rows. |
| `nyc_food_access_data_COMPLETE_WITH_FLAGS.csv` | 1,278 | Same columns plus `data_quality`. |
| `nyc_food_access_data_ORIGINAL.csv` | 1,278 | Same shape as the complete file, without the flags column. |
| `manual_data/community_fridges.csv` | 20 | Hand-entered fridges. Missing `local_items_selling` and `social_media_website2`. |
| `manual_data/urban_farms.csv` | 35 | Hand-entered farms. Same missing columns. `merge_manual_data.py` does not read this file. |

`clean_csv.py` treats a row as broken when the name contains a newline, the name is longer than 150 characters, or the address is empty and the name is longer than 50 characters. Run on the current complete file, it keeps 1,235 rows and drops 44, all of them from the farmers-market count (63 down to 19). It deletes those rows. It does not split them apart.

In that same complete file, 986 rows have a latitude, 448 have hours, 685 have an owner, 41 have a website, and 5 have a contact. `local_items_selling` and `social_media_website2` are empty there too.

## Setup

Tested on Python 3.12.3. Chrome or Chromium is required only for the Selenium sources. On the machine used to check this file, Selenium Manager (bundled with the `selenium` package) started the installed Chrome; a separate ChromeDriver download was not required.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`.

`requirements.txt` installs `requests`, `beautifulsoup4`, `pandas`, `lxml`, `selenium`, `pdfplumber`, `geopy`, and `tqdm`. That is enough for `main.py`, `clean_csv.py`, and `merge_manual_data.py`.

`ocr_lungs_map.py` also needs the `pytesseract` package, Pillow (already pulled in by `pdfplumber`), and a Tesseract binary on `PATH`. Those are not installed by the steps above.

`setup_selenium.sh` downloads ChromeDriver from `chromedriver.storage.googleapis.com`, which is the old ChromeDriver host. Current Chrome releases are not published there. Prefer Selenium Manager, which runs when `SeleniumScraper` calls `webdriver.Chrome(...)`.

## Usage

A full run requests every configured URL, and it geocodes addresses that have no coordinates. That takes a long time, depends on the network, and sends traffic to the organizations listed above. Read the responsible-scraping section before starting one. This documentation change did not include a live run.

```bash
python main.py
```

The CSV and the log are written in the current directory. Generated CSVs and logs are gitignored, except the snapshots named in `.gitignore`.

Append the hand-entered fridges onto a scrape, then drop rows that share a name and address:

```bash
python merge_manual_data.py nyc_food_access_data_YYYYMMDD_HHMMSS.csv
```

An optional second argument sets the output path. The default name is `nyc_food_access_data_complete_<timestamp>.csv`. The script reads `manual_data/community_fridges.csv` only.

Drop the multiline farmers-market rows from the checked-in complete file:

```bash
python clean_csv.py
```

That command is hardcoded to read `nyc_food_access_data_COMPLETE.csv` and write `nyc_food_access_data_CLEAN.csv`. The output name is gitignored.

To add a source, add a dictionary to the matching list in `config.py` (`name`, `url`, `type`, and `use_selenium` or `format` when needed). Sources that do not match a page-specific branch go through the generic HTML, JSON, or Selenium parser.

## Responsible scraping

The scraper exists to fill a public food-access map. The sites it calls publish gardens, markets, and pantries for people who need them. Treat that as the limit of the tool.

What the code actually does:

- It sends a desktop Chrome `User-Agent`, not a bot name or a contact address.
- After a successful download through `BaseScraper.get_page()` (HTML pages and PDFs), it sleeps 2 seconds. Socrata pagination, the ArcGIS queries, and Nominatim calls do not go through that method.
- `RATE_LIMIT` in `config.py` (`requests_per_minute` 30, `delay_between_requests` 2) is never read.
- Nothing fetches or parses `robots.txt`.
- Nominatim is called with user agent `nyc_food_access_scraper`. Successful lookups are not spaced out. The public Nominatim usage policy asks for at most one request per second, a descriptive user agent, and caching. The in-memory cache covers repeats inside one run only.
- Selenium drives a headless browser, including against Google My Maps.

Before a full run:

- Check each site's terms and `robots.txt`. Skip a source that disallows automated collection. The NYC Open Data APIs are the durable source for GreenThumb gardens and FRESH stores; several HTML and dashboard entries overlap that dataset.
- Keep the 2-second pause, and add a delay of at least one second around Nominatim. For a large refresh, use a geocoder you operate instead of the public Nominatim instance.
- Identify the project in the user agent, with a contact, if you keep running it.
- Leave `source_url` on every row so the map can credit the organization the record came from.
- Phone numbers and emails in the output were published by those organizations. Don't republish them for a different purpose.
- Don't raise the request rate, don't route around a block, and don't run the Selenium sources on a schedule. They are the most brittle parsers and the easiest ones to aim at a site that does not want browser automation.

## Limitations

These are properties of the code as it is, not a backlog someone has committed to.

- Most HTML parsers guess CSS classes. The October 2025 notes say many of those pages returned nothing. Local Harvest, the GreenThumb API, and the NYC Food Help Finder path are the ones written against a specific structure.
- Google My Maps KML parsing is not implemented. The Selenium fallback reads class names out of the page and is unlikely to return a clean place list.
- The ArcGIS scraper guesses three service names. If none of them answer, that source adds zero rows. The dashboard's "1000+" figure is not something this code reproduces on its own.
- PDF text extraction both tables and free text, so markets can be duplicated or smashed into one cell. `clean_csv.py` exists because of that.
- Geocoding always appends `, New York`, including for Local Harvest, which already appends `, USA` before calling the geocoder. Places outside New York can be missed or pinned to the wrong city.
- `SEARCH_KEYWORDS` in `config.py` is unused. There is no search step that discovers new sites.
- `merge_manual_data.py` ignores `manual_data/urban_farms.csv`.
- There is no `LICENSE` file. The previous README called the project MIT; that statement is not backed by a license in the tree. Ask Shay before you reuse the code or the snapshots.

## Other notes in the repo

`PROJECT_SUMMARY.md`, `FINAL_SUMMARY.md`, `SCRAPER_STATUS.md`, `DATA_GAPS_AND_SOLUTIONS.md`, `COMMUNITY_FRIDGE_CHALLENGE.md`, `DEBUGGING_NOTES.md`, and `SELENIUM_SETUP.md` are working notes from October 2025. Use them as history. Use this file for how the project runs.
