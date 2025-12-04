"""Quick test with REAL data - No AI (faster)."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import load_config
from src.scraper import search_places
from src.filters import is_good_lead, transform_place
from src.storage import append_to_csv

print("🚀 QUICK TEST - REAL DATA")
print("=" * 80)

# Load config
config = load_config()
serpapi_key = config['SERPAPI_KEY']

# Test with 2 queries
queries = [
    "baby care in Delhi, India",
    "day care centre in Gurgaon, India"
]

all_leads = []

for query in queries:
    print(f"\n🔍 Scraping: {query}")
    places = search_places(query, serpapi_key)
    print(f"   Found: {len(places)} businesses")
    
    # Filter
    for place in places:
        if is_good_lead(place):
            lead = transform_place(place, query)
            all_leads.append(lead)
            print(f"   ✅ {lead['business_name']} - {lead['rating']}★ ({lead['reviews_count']} reviews)")

print()
print("=" * 80)
print(f"📊 Total qualified leads: {len(all_leads)}")

if all_leads:
    # Save to CSV
    append_to_csv(all_leads)
    print(f"✅ Saved to: data/all_leads.csv")
    print()
    
    # Show sample
    print("📋 Sample Lead:")
    lead = all_leads[0]
    print(f"   Business: {lead['business_name']}")
    print(f"   City: {lead['city']}")
    print(f"   Rating: {lead['rating']}★")
    print(f"   Reviews: {lead['reviews_count']}")
    print(f"   Phone: {lead['phone']}")
    print(f"   Address: {lead['city']}, {lead['state']}, {lead['country']}")
    print(f"   Place ID: {lead['place_id']}")

print()
print("🎉 REAL DATA TEST COMPLETE!")
