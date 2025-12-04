"""Test REAL data scraping with SerpAPI."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import load_config
from src.scraper import search_places
from src.filters import is_good_lead, transform_place

print("🚀 TESTING REAL DATA SCRAPING")
print("=" * 80)

# Load config
config = load_config()
serpapi_key = config.get('SERPAPI_KEY')

if not serpapi_key:
    print("❌ SERPAPI_KEY not found in config!")
    exit(1)

print(f"✅ SerpAPI Key: {serpapi_key[:20]}...")
print()

# Test query
query = "baby care in Delhi, India"
print(f"📝 Testing query: {query}")
print()

# Scrape REAL data
print("🔍 Scraping REAL businesses...")
places = search_places(query, serpapi_key)

print()
print(f"📊 Found {len(places)} businesses")
print("=" * 80)
print()

# Show results
for idx, place in enumerate(places[:5], 1):
    print(f"[{idx}] {place['title']}")
    print(f"    Rating: {place.get('rating', 'N/A')}★")
    print(f"    Reviews: {place.get('reviews', 0)}")
    print(f"    Address: {place.get('address', 'N/A')}")
    print(f"    Phone: {place.get('phone', 'N/A')}")
    print(f"    Website: {place.get('website', 'None')}")
    print(f"    Place ID: {place.get('place_id', 'N/A')}")
    
    # Check if good lead
    if is_good_lead(place):
        print(f"    ✅ GOOD LEAD (No website, good rating)")
    else:
        print(f"    ❌ Not qualified")
    print()

print("=" * 80)
print("🎉 TEST COMPLETE!")
print()

# Count qualified leads
qualified = [p for p in places if is_good_lead(p)]
print(f"📊 Summary:")
print(f"   Total found: {len(places)}")
print(f"   Qualified leads: {len(qualified)}")
print(f"   Qualification rate: {len(qualified)/len(places)*100:.1f}%")
