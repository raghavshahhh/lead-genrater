"""Quick test of lead generation system."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import load_config
from src.queries import generate_queries
from src.scraper_free import search_places_free
from src.filters import is_good_lead, transform_place
from src.storage import append_to_sheet, append_to_csv

print("🚀 Starting Quick Test...")
print("=" * 80)

# Load config
config = load_config()
print(f"✅ Config loaded")
print(f"   MAX_LEADS: {config['MAX_LEADS_PER_RUN']}")
print(f"   MIN_RATING: {config['MIN_RATING']}")
print(f"   MIN_REVIEWS: {config['MIN_REVIEWS']}")
print()

# Generate ONE query for testing
queries = ["baby care in Delhi, India"]
print(f"📝 Testing with query: {queries[0]}")
print()

# Scrape
print("🔍 Scraping...")
places = search_places_free(queries[0], max_results=5)
print(f"   Found {len(places)} businesses")
print()

# Filter
qualified_leads = []
for place in places:
    if is_good_lead(place):
        lead = transform_place(place, queries[0])
        qualified_leads.append(lead)
        print(f"✅ Qualified: {lead['business_name']}")
        print(f"   Rating: {lead['rating']}★, Reviews: {lead['reviews_count']}")
        print(f"   City: {lead['city']}, Phone: {lead['phone']}")
        print()

print(f"📊 Total qualified leads: {len(qualified_leads)}")
print()

if qualified_leads:
    # Store to Google Sheets
    print("💾 Storing to Google Sheets...")
    try:
        append_to_sheet(
            qualified_leads,
            config['GOOGLE_SHEET_ID'],
            config['GOOGLE_SERVICE_ACCOUNT_JSON']
        )
        print("✅ Successfully stored to Google Sheets!")
    except Exception as e:
        print(f"❌ Error storing to Google Sheets: {str(e)}")
    
    # Store to CSV
    print("💾 Storing to CSV...")
    append_to_csv(qualified_leads)
    print("✅ Successfully stored to CSV!")
    print()

print("=" * 80)
print("🎉 Test Complete!")
print()
print("📋 Next Steps:")
print("1. Check your Google Sheet for the leads")
print("2. Check data/all_leads.csv for backup")
print("3. Run full system: python src/main_free.py")
