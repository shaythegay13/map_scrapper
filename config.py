"""
Complete Configuration file for NYC Food Access Data Scraper - ALL 45 UNIQUE SOURCES
"""

# Geographic boundaries
GEOGRAPHIC_BOUNDS = {
    "nyc_boroughs": ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"],
    "counties": ["Westchester County", "Nassau County", "Suffolk County"],
    "cities": ["Yonkers"],
    "nj_distance_miles": 50,
    "center_coords": (40.7128, -73.9352)
}

# Data sources organized by type
DATA_SOURCES = {
    "api_sources": [
        {
            "name": "NYC Open Data - GreenThumb Gardens API",
            "url": "https://data.cityofnewyork.us/resource/p78i-pat6.json",
            "type": "community_garden",
            "format": "socrata_api"
        },
        {
            "name": "NYC Open Data - FRESH Food Stores",
            "url": "https://data.cityofnewyork.us/resource/3ayg-qpzm.json",
            "type": "food_store",
            "format": "socrata_api"
        }
    ],
    
    "html_sources": [
        {
            "name": "NYC Parks GreenThumb Community Gardens",
            "url": "https://www.nycgovparks.org/greenthumb/community-gardens",
            "type": "community_garden"
        },
        {
            "name": "LUNGS NYC Gardens & Greenspaces",
            "url": "https://lungsnyc.org/gardens-greenspaces/",
            "type": "community_garden"
        },
        {
            "name": "Community Fridge Finder Browse",
            "url": "https://www.communityfridgefinder.com/browse",
            "type": "community_fridge",
            "note": "Map-based, difficult to scrape"
        },
        {
            "name": "Freedge NYC",
            "url": "https://www.freedge.org/locations",
            "type": "community_fridge"
        },
        {
            "name": "NYC Mutual Aid Network - Community Fridges",
            "url": "https://mutualaid.nyc/resources/",
            "type": "community_fridge"
        },
        {
            "name": "Bed-Stuy Strong Community Fridge",
            "url": "https://www.bedstuystrong.com/community-fridge",
            "type": "community_fridge"
        },
        {
            "name": "One Love Community Fridge - Fridges",
            "url": "https://www.onelovecommunityfridge.org/fridges",
            "type": "community_fridge",
            "use_selenium": True
        },
        {
            "name": "One Love Community Fridge - Main",
            "url": "https://www.onelovecommunityfridge.org/",
            "type": "community_fridge",
            "use_selenium": True
        },
        {
            "name": "Manhattan Land Trust - Our Gardens",
            "url": "https://www.manhattanlandtrust.org/our-gardens/",
            "type": "community_garden"
        },
        {
            "name": "Brooklyn Queens Land Trust - Our Gardens",
            "url": "https://bqlt.org/our-gardens",
            "type": "community_garden"
        },
        {
            "name": "Brooklyn Queens Land Trust - Main",
            "url": "https://bqlt.org/",
            "type": "community_garden"
        },
        {
            "name": "Bronx Land Trust - Our Gardens",
            "url": "https://www.bronxlandtrust.org/ourgardens",
            "type": "community_garden"
        },
        {
            "name": "Bronx Land Trust - Main",
            "url": "https://www.bronxlandtrust.org/",
            "type": "community_garden"
        },
        {
            "name": "NY Alternative Land Trust",
            "url": "https://www.nyalt.org/",
            "type": "community_garden"
        },
        {
            "name": "NYRP Gardens and Parks",
            "url": "https://www.nyrp.org/en/gardens-and-parks/",
            "type": "community_garden"
        },
        {
            "name": "Zachary Schulman Garden Leaders",
            "url": "https://zacharyschulman.com/gardenleaders",
            "type": "community_garden"
        },
        {
            "name": "Food Bank NYC - Get Help",
            "url": "https://www.foodbanknyc.org/get-help/",
            "type": "food_bank"
        },
        {
            "name": "NYC Food Help Finder",
            "url": "https://finder.nyc.gov/foodhelp/locations?mView=map",
            "type": "food_bank",
            "use_selenium": True
        },
        {
            "name": "City Harvest Food Map",
            "url": "https://www.cityharvest.org/food-map/",
            "type": "food_bank",
            "use_selenium": True
        },
        {
            "name": "GrowNYC Greenmarket - Our Markets",
            "url": "https://www.grownyc.org/greenmarket/ourmarkets",
            "type": "farmers_market"
        },
        {
            "name": "Secret NYC Farmers Markets",
            "url": "https://secretnyc.co/farmers-markets-nyc/",
            "type": "farmers_market"
        },
        {
            "name": "NYC Tourism - Best Farmers Markets",
            "url": "https://www.nyctourism.com/articles/best-farmers-markets-new-york-city/",
            "type": "farmers_market"
        },
        {
            "name": "Local Harvest NYC Farmers Markets",
            "url": "https://www.localharvest.org/search.jsp?map=1&lat=40.75&lon=-73.99&scale=11&ty=1",
            "type": "farmers_market"
        },
        {
            "name": "Local Harvest NYC CSAs",
            "url": "https://www.localharvest.org/search.jsp?map=1&lat=40.75&lon=-73.99&scale=11&ty=6",
            "type": "csa"
        },
        {
            "name": "Just Food Value Chain Map",
            "url": "https://www.justfood.org/value-chain-map?tags=community-%20run%20farmers%20market%20site",
            "type": "farmers_market"
        },
        {
            "name": "Public Markets NYC - Jamaica Farmers Market",
            "url": "https://publicmarkets.nyc/jamaica-farmers-market",
            "type": "farmers_market"
        },
        {
            "name": "Queens Farm - Farmstand",
            "url": "https://www.queensfarm.org/farmstand/",
            "type": "farm"
        },
        {
            "name": "South Bronx Farmers Market",
            "url": "http://southbronxfarmersmarket.com/",
            "type": "farmers_market"
        },
        {
            "name": "Sprout Up - Exploring a Farm",
            "url": "https://www.sproutup.org/exploring-a-farm",
            "type": "urban_farm"
        },
        {
            "name": "Garden Kitchen Lab - Our Farms",
            "url": "https://gardenkitchenlab.org/our-farms/",
            "type": "urban_farm"
        },
        {
            "name": "Project Evergreen - GreenCare for Communities",
            "url": "https://projectevergreen.org/greencare-for-communities/",
            "type": "community_garden"
        },
        {
            "name": "NY Agriculture - Farmers Markets",
            "url": "https://agriculture.ny.gov/farmersmarkets",
            "type": "farmers_market"
        },
        {
            "name": "Wellspring Forest Farm",
            "url": "https://www.wellspringforestfarm.com/",
            "type": "farm"
        },
        {
            "name": "Farming with Trees",
            "url": "https://www.farmingwithtrees.org/home",
            "type": "farm"
        },
        {
            "name": "The Last Farm in NYC - Markets & CSAs",
            "url": "https://thelastfarminnewyorkcity.com/markets-csas/",
            "type": "csa"
        },
        {
            "name": "NYBG Edible Academy",
            "url": "https://www.nybg.org/education/childrens-education/edible-academy/",
            "type": "urban_farm"
        },
        {
            "name": "EHR90Z Wix Site Projects",
            "url": "https://ehr90z.wixsite.com/my-site-2/projects-3",
            "type": "community_garden"
        },
        {
            "name": "Bonton Farms",
            "url": "https://bontonfarms.org/",
            "type": "urban_farm"
        },
        {
            "name": "UB Healthy Project Farmers Market",
            "url": "https://ubhealthyproject.org/farmersmarket/",
            "type": "farmers_market"
        }
    ],
    
    "pdf_sources": [
        {
            "name": "NYC DOH Farmers Markets Map PDF",
            "url": "https://www.nyc.gov/assets/doh/downloads/pdf/cdp/farmers-markets-map.pdf",
            "type": "farmers_market"
        },
        {
            "name": "NY Agriculture FMNP Schedule PDF",
            "url": "https://agriculture.ny.gov/system/files/documents/2025/06/fmnpmarketschedulescountiesnyc.pdf",
            "type": "farmers_market"
        },
        {
            "name": "GrowNYC Market Map PDF",
            "url": "https://www.grownyc.org/files/gmkt/map.pdf",
            "type": "farmers_market"
        }
    ],
    
    "map_sources": [
        {
            "name": "NYC ArcGIS Community Gardens Dashboard (1000+ locations)",
            "url": "https://nyc.maps.arcgis.com/apps/dashboards/7d3e668dfcdd4bce93275dae44fcd3dd",
            "type": "community_garden",
            "format": "arcgis"
        },
        {
            "name": "Community Fridge Google Map",
            "url": "https://www.google.com/maps/d/u/0/viewer?mid=1c4jHrGl0ymGUXPDUPXCTmKdMD00FgJzl&ll=40.69109846326807%2C-73.97261285000002&z=13",
            "type": "community_fridge",
            "format": "google_maps"
        },
        {
            "name": "Farmers Markets Google Map 1",
            "url": "https://www.google.com/maps/d/u/0/viewer?mid=1fqTOVOwP6fj4NXOpFHT2Y48e3zEghRiJ&ll=40.760619747874344%2C-73.98352704302141&z=11",
            "type": "farmers_market",
            "format": "google_maps"
        },
        {
            "name": "Farmers Markets Google Map 2",
            "url": "https://www.google.com/maps/d/u/0/viewer?mid=1fqTOVOwP6fj4NXOpFHT2Y48e3zEghRiJ&ll=40.76009965033155%2C-73.83795819536516&z=11",
            "type": "farmers_market",
            "format": "google_maps"
        }
    ],
    
    "image_sources": [
        {
            "name": "Project Evergreen NYC Map 2025 Image",
            "url": "https://projectevergreen.org/wp-content/uploads/2025/03/PE-NYC-Map-2025_001.jpg",
            "type": "community_garden",
            "note": "Image file - requires OCR or manual extraction"
        }
    ],
    
    "data_portal_sources": [
        {
            "name": "NYC Open Data - GreenThumb Garden Info (About Data)",
            "url": "https://data.cityofnewyork.us/dataset/GreenThumb-Garden-Info/p78i-pat6/about_data",
            "type": "community_garden",
            "note": "Data portal page - use API instead"
        },
        {
            "name": "NYC Open Data - GreenThumb Garden Info (Data Preview)",
            "url": "https://data.cityofnewyork.us/dataset/GreenThumb-Garden-Info/p78i-pat6/data_preview",
            "type": "community_garden",
            "note": "Data portal page - use API instead"
        }
    ]
}

# Output schema
OUTPUT_FIELDS = [
    "name",
    "address",
    "neighborhood",
    "lat",
    "long",
    "description",
    "type",
    "open_hours",
    "owner",
    "local_items_selling",
    "contact_information",
    "social_media_website1",
    "social_media_website2",
    "source_url",
    "last_updated"
]

# Rate limiting settings
RATE_LIMIT = {
    "requests_per_minute": 30,
    "delay_between_requests": 2
}

# Search keywords for discovering additional sources
SEARCH_KEYWORDS = [
    "NYC community gardens",
    "NYC farmers markets",
    "NYC urban farms",
    "NYC community fridges",
    "NYC food banks",
    "NYC food pantries",
    "NYC CSA programs",
    "Westchester community gardens",
    "Long Island farmers markets",
    "Yonkers food access",
    "Northern New Jersey community gardens",
    "Hudson County farmers markets"
]
