"""
Quick test for PREMIUM CLIENT lead generation.
Tests the quality filtering and international targeting.
"""

import sys
sys.path.insert(0, 'src')

from lead_quality_filter import LeadQualityScorer, filter_serious_clients_only
from queries import CITIES, CATEGORIES

print("""
╔══════════════════════════════════════════════════════════╗
║     PREMIUM LEAD GENERATION - QUICK TEST                 ║
╚══════════════════════════════════════════════════════════╝
""")

# Test 1: Show international cities
print("\n🌍 INTERNATIONAL CITIES TARGETED:")
print(f"   Total: {len(CITIES)} cities")
print("\n   Top 10 cities:")
for i, city in enumerate(CITIES[:10], 1):
    print(f"   {i}. {city}")

# Test 2: Show high-value categories
print(f"\n💰 HIGH-VALUE BUSINESS CATEGORIES:")
print(f"   Total: {len(CATEGORIES)} categories")
print("\n   Top 10 highest-paying:")
for i, category in enumerate(CATEGORIES[:10], 1):
    print(f"   {i}. {category}")

# Test 3: Test quality scoring
print(f"\n🎯 QUALITY SCORING TEST:")
print("   Testing with sample businesses...\n")

test_businesses = [
    {
        'title': 'Goldman & Partners Law Firm',
        'type': 'corporate law firm',
        'rating': 4.9,
        'reviews': 450,
        'website': None,  # No website = opportunity!
        'phone': '+1-212-555-0100',
        'address': 'New York, USA'
    },
    {
        'title': 'Luxury Real Estate International',
        'type': 'luxury real estate',
        'rating': 4.8,
        'reviews': 320,
        'website': 'oldwebsite.com',
        'phone': '+44-20-5555-0200',
        'address': 'London, UK'
    },
    {
        'title': 'Dubai Investment Group',
        'type': 'investment firm',
        'rating': 4.7,
        'reviews': 280,
        'website': None,
        'phone': '+971-4-555-0300',
        'address': 'Dubai, UAE'
    },
    {
        'title': 'TechVentures Capital',
        'type': 'venture capital',
        'rating': 4.6,
        'reviews': 150,
        'website': 'techvc.com',
        'phone': '+1-415-555-0400',
        'address': 'San Francisco, USA'
    },
    {
        'title': 'Budget Babysitting Services',
        'type': 'daycare',
        'rating': 4.2,
        'reviews': 15,
        'website': 'babysit.com',
        'phone': '+1-555-0500',
        'address': 'Mumbai, India'
    },
    {
        'title': 'Elite Cosmetic Surgery Center',
        'type': 'cosmetic surgery',
        'rating': 4.9,
        'reviews': 500,
        'website': None,
        'phone': '+1-310-555-0600',
        'address': 'Los Angeles, USA'
    }
]

# Score each business
for business in test_businesses:
    score = LeadQualityScorer.calculate_quality_score(business)
    business['quality_score'] = score
    
    # Determine if premium
    is_premium = score >= 70
    emoji = "✅" if is_premium else "❌"
    
    print(f"{emoji} {business['title']}")
    print(f"   Type: {business['type']}")
    print(f"   Location: {business['address']}")
    print(f"   Rating: {business['rating']} ({business['reviews']} reviews)")
    print(f"   Quality Score: {score:.0f}/100 {'(PREMIUM CLIENT!)' if is_premium else '(Low quality)'}")
    print()

# Test 4: Filter for premium clients only
print("\n🏆 FILTERING FOR PREMIUM CLIENTS ONLY (Score >= 70):")
premium_clients = [b for b in test_businesses if b['quality_score'] >= 70]

print(f"   Found {len(premium_clients)}/{len(test_businesses)} PREMIUM clients:\n")
for i, client in enumerate(premium_clients, 1):
    print(f"   {i}. {client['title']} - {client['quality_score']:.0f}/100")
    print(f"      📍 {client['address']}")
    print(f"      💼 {client['type']}")
    print()

# Test 5: Show query examples
print("\n📝 SAMPLE SEARCH QUERIES:")
print("   (These will be used for FREE scraping)\n")
sample_queries = [
    f"{CATEGORIES[0]} in {CITIES[0]}",
    f"{CATEGORIES[1]} in {CITIES[1]}",
    f"{CATEGORIES[2]} in {CITIES[2]}",
    f"{CATEGORIES[3]} in {CITIES[3]}",
    f"{CATEGORIES[4]} in {CITIES[4]}",
]
for i, query in enumerate(sample_queries, 1):
    print(f"   {i}. {query}")

print("\n" + "="*60)
print("✅ TEST COMPLETE!")
print("="*60)
print("\n🚀 Ready to generate PREMIUM leads!")
print("\nRun: python src/main_premium_clients.py")
print("\nThis will:")
print("  ✅ Target HIGH-PAYING international clients")
print("  ✅ Filter for SERIOUS businesses only (score >= 70)")
print("  ✅ Use 100% FREE scraping (no API costs)")
print("  ✅ Focus on USA, UK, UAE, Canada, Australia, Europe")
print("  ✅ Prioritize: Law firms, Finance, Real Estate, Tech, Healthcare")
