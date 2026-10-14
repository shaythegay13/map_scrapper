# Data Gaps & Solutions

> Working notes from October 2025. Counts in this file can disagree with `config.py` and the CSV snapshots. [README.md](README.md) is the current description.

## Current Status

### ✅ What We Have (682 records):
- **Community Gardens**: 624 ✓
- **Farmers Markets**: 51 ✓
- **Urban Farms**: 6 ✓
- **CSA Programs**: 1 ✓

### ❌ What's Missing (0 records):
- **Community Fridges**: 0 ❌
- **Food Banks & Pantries**: 0 ❌
- **Farms** (separate from urban farms): Need more

## Why Data is Missing

### Community Fridges
**Problem**: All HTML sources returned 0 records
- communityfridgefinder.com - complex JavaScript
- onelovecommunityfridge.org - anti-scraping measures
- Google Maps - requires special handling

**Why it failed**: 
- Sites use React/dynamic loading
- Selenium selectors don't match actual page structure
- Data embedded in JavaScript, not HTML

### Food Banks & Pantries
**Problem**: All sources returned 0 records
- foodbanknyc.org - JavaScript-heavy
- finder.nyc.gov - requires API key or complex interaction
- cityharvest.org - dynamic map widget

**Why it failed**:
- No public APIs available
- Interactive maps with protected data
- Selenium couldn't extract from JavaScript frameworks

## Solutions

### Option 1: Manual Data Collection (FASTEST)
**Community Fridges** (~50 locations):
- Visit onelovecommunityfridge.org manually
- Copy data to spreadsheet
- Import to CSV

**Food Banks** (~200 locations):
- Use NYC Human Resources Admin data
- Download from Feeding America locator
- 211 NYC database export

**Pros**: 
- Quick (1-2 hours)
- Accurate data
- Can verify/clean manually

**Cons**:
- Manual work
- Not automated for updates

### Option 2: Fix Selenium Scrapers (MEDIUM)
**Steps**:
1. Manually inspect each site's HTML structure
2. Update selectors in selenium_scraper.py
3. Add screenshots for debugging
4. Handle dynamic loading properly

**Estimated time**: 4-6 hours
**Success rate**: 60-70% (some sites may still block)

### Option 3: Find Alternative Data Sources (BEST LONG-TERM)
**Community Fridges**:
- Contact One Love directly for data export
- Use Instagram/social media scraping (if permitted)
- Partner with NYC food access organizations

**Food Banks**:
- NYC Open Data - look for HRA datasets
- Feeding America API (if available)
- 211 NYC partnership
- USDA Food Access Research Atlas

### Option 4: Hybrid Approach (RECOMMENDED)
1. **Immediate**: Manually add top 20-30 community fridges
2. **Short-term**: Fix Selenium for 1-2 key sites
3. **Long-term**: Partner with data providers

## Recommended Next Steps

### Step 1: Quick Manual Addition (30 min)
Create `manual_data/community_fridges.csv` with known locations:
```csv
name,address,neighborhood,type
Bed-Stuy Fridge,1234 Bedford Ave,Brooklyn,community_fridge
Bushwick Fridge,567 Bushwick Ave,Brooklyn,community_fridge
...
```

### Step 2: Find NYC Food Bank Data (1 hour)
Search for:
- NYC HRA food assistance locations
- Emergency Food Assistance Program (EFAP) data
- NYC Coalition Against Hunger database

### Step 3: Test One Selenium Fix (1 hour)
Pick ONE site (e.g., onelovecommunityfridge.org):
- Inspect actual HTML
- Update selectors
- Test thoroughly
- If successful, apply to others

## Data Source Recommendations

### For Community Fridges:
1. **One Love Community Fridge** - has ~30 fridges
   - Manual: Visit site, copy data
   - API: Contact them directly

2. **NYC Mutual Aid Networks** - crowdsourced data
   - Check Google Sheets/Airtable bases
   - Community-maintained lists

3. **Instagram/Social Media** - many fridges post locations
   - #communityfridge #nyc
   - Geo-tagged posts

### For Food Banks/Pantries:
1. **NYC Human Resources Admin** - official list
   - https://www1.nyc.gov/site/hra/help/food-assistance.page

2. **Feeding America** - national database
   - https://www.feedingamerica.org/find-your-local-foodbank

3. **NYC Coalition Against Hunger** - comprehensive list
   - https://www.nyccah.org/find-food

4. **City Harvest** - partner organizations
   - Contact for partner location data

5. **Food Bank For NYC** - distribution sites
   - Request location export

## Immediate Action Plan

### Today (2 hours):
1. ✅ Remove food scrap sites (DONE)
2. ⏳ Manually add 20-30 community fridges
3. ⏳ Find and add NYC food bank dataset

### This Week:
1. Debug one Selenium scraper thoroughly
2. Contact organizations for data partnerships
3. Create manual data import process

### Long-term:
1. Build relationships with food access orgs
2. Set up automated data updates
3. Create community submission form

## Current Recommendation

**For your immediate map needs**, I recommend:

1. **Use the 682 records we have** as the base
2. **Manually add 30-50 community fridges** (1 hour work)
3. **Find one good food bank dataset** and import it
4. **Total result**: ~900-1000 locations covering all categories

This gives you a complete, usable map while we work on automation for future updates.

Would you like me to:
A) Help create a manual CSV template for community fridges?
B) Search for downloadable food bank datasets?
C) Debug one specific Selenium scraper?
D) All of the above?
