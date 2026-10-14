# Community Fridge Data Challenge

> Working notes from October 2025. Counts in this file can disagree with `config.py` and the CSV snapshots. [README.md](README.md) is the current description.

## Current Status

**Community Fridges Found**: 6-7 (from One Love + Freedge)

## Why So Few?

### The Reality of Community Fridge Data:

1. **Grassroots & Decentralized**
   - No central database or registry
   - Run by individual community groups
   - Locations change frequently
   - Many are temporary/seasonal

2. **Social Media Based**
   - Most documented on Instagram (#communityfridge #nyc)
   - Facebook community groups
   - Twitter threads
   - Not on traditional websites

3. **Map-Based Platforms**
   - Community Fridge Finder - interactive map (can't scrape)
   - Google My Maps - embedded JavaScript (blocked)
   - Requires user interaction to view data

4. **No Public APIs**
   - Unlike food banks (NYC Open Data has 512!)
   - Unlike gardens (GreenThumb API has 624!)
   - Community fridges have no government/official tracking

## What We've Tried:

✅ **One Love Community Fridge** - 6 fridges (WORKING!)
✅ **Freedge NYC** - 1 fridge (WORKING!)
❌ **Community Fridge Finder** - Map-based, can't extract
❌ **Google My Maps** - JavaScript blocked
❌ **A New World in Our Hearts** - Site doesn't exist

## Realistic Expectations:

Based on research, NYC has approximately **30-50 active community fridges** at any given time. They include:
- One Love network: ~6-10
- Bed-Stuy Strong: ~2-3
- Bushwick Fridge: ~2-3
- Various mutual aid groups: ~15-20
- Individual/unaffiliated: ~10-15

**We can scrape**: ~10-15 (from known websites)
**We cannot scrape**: ~20-35 (social media, maps, temporary)

## Solutions:

### Option 1: Accept Current Coverage (Recommended)
- We have 6-7 fridges from reliable sources
- These are the most established/permanent ones
- Focus on other data types where we have better coverage

### Option 2: Manual Supplementation
- Manually add 10-20 known fridges from:
  - Instagram posts
  - Community group websites
  - Local news articles
- Update quarterly as fridges come/go

### Option 3: Social Media Scraping (Complex)
- Scrape Instagram hashtags (requires API/authentication)
- Parse Facebook groups (against TOS)
- Not recommended due to legal/technical issues

### Option 4: Community Submission Form
- Create a web form for community members to submit fridge locations
- Verify submissions manually
- Most sustainable long-term solution

## Comparison with Other Data Types:

| Type | Count | Coverage | Source Quality |
|------|-------|----------|----------------|
| Food Banks | 511 | ✅ Excellent | Official NYC data |
| Community Gardens | 624 | ✅ Excellent | GreenThumb API |
| Farmers Markets | 51 | ✅ Good | Multiple sources |
| **Community Fridges** | **6-7** | **⚠️ Limited** | **Grassroots only** |
| CSAs | 1-30 | ⚠️ Improving | Local Harvest |

## Recommendation:

**Accept 6-7 community fridges for now** because:
1. They're from the most reliable/permanent sources
2. Community fridges are inherently hard to track
3. We have excellent coverage of other food access types
4. Can supplement manually if needed

**Total dataset will still be ~1,220+ records** covering:
- ✅ 511 Food Banks/Pantries
- ✅ 624 Community Gardens  
- ✅ 51 Farmers Markets
- ✅ 10-30 CSAs (after fix)
- ✅ 6-7 Community Fridges
- ✅ 6 Urban Farms

This is a comprehensive, usable dataset for your food access map!
