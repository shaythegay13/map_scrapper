# Quick start

Setup and behavior are documented in [README.md](README.md). This page is only the commands.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Collect from every source in `config.py` (this hits the network; read the responsible-scraping section first):

```bash
python main.py
```

That writes `nyc_food_access_data_YYYYMMDD_HHMMSS.csv` and `scraper_YYYYMMDD_HHMMSS.log` in the current directory.

```bash
python merge_manual_data.py path/to/scraped.csv
python clean_csv.py
```

`merge_manual_data.py` appends `manual_data/community_fridges.csv` only. `clean_csv.py` reads `nyc_food_access_data_COMPLETE.csv` and writes `nyc_food_access_data_CLEAN.csv`.

The checked-in complete snapshot has 1,279 records. A fresh run will not match that file, and several HTML parsers are generic guesses. Details, source list, and limits are in the README.
