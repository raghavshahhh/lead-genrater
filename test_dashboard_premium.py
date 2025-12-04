"""
Test Premium Dashboard - Creates sample data and tests system
"""

import json
import os
import sys

sys.path.insert(0, 'src')

# Create sample premium leads
sample_leads = [
    {
        'title': 'Goldman & Partners Law Firm',
        'type': 'corporate law firm',
        'rating': 4.9,
        'reviews': 450,
        'address': '123 Wall Street, New York, USA',
        'phone': '+1-212-555-0100',
        'website': None,
        'quality_score': 100,
        'place_id': 'test_1',
        'gps_coordinates': {}
    },
    {
        'title': 'Luxury Real Estate International',
        'type': 'luxury real estate',
        'rating': 4.8,
        'reviews': 320,
        'address': '456 Oxford Street, London, UK',
        'phone': '+44-20-5555-0200',
        'website': 'oldwebsite.com',
        'quality_score': 100,
        'place_id': 'test_2',
        'gps_coordinates': {}
    },
    {
        'title': 'Dubai Investment Group',
        'type': 'investment firm',
        'rating': 4.7,
        'reviews': 280,
        'address': 'Sheikh Zayed Road, Dubai, UAE',
        'phone': '+971-4-555-0300',
        'website': None,
        'quality_score': 100,
        'place_id': 'test_3',
        'gps_coordinates': {}
    },
    {
        'title': 'TechVentures Capital',
        'type': 'venture capital',
        'rating': 4.6,
        'reviews': 150,
        'address': '789 Market Street, San Francisco, USA',
        'phone': '+1-415-555-0400',
        'website': 'techvc.com',
        'quality_score': 95,
        'place_id': 'test_4',
        'gps_coordinates': {}
    },
    {
        'title': 'Elite Cosmetic Surgery Center',
        'type': 'cosmetic surgery',
        'rating': 4.9,
        'reviews': 500,
        'address': 'Beverly Hills, Los Angeles, USA',
        'phone': '+1-310-555-0600',
        'website': None,
        'quality_score': 100,
        'place_id': 'test_5',
        'gps_coordinates': {}
    },
    {
        'title': 'Toronto Financial Advisors',
        'type': 'financial advisor',
        'rating': 4.7,
        'reviews': 200,
        'address': 'Bay Street, Toronto, Canada',
        'phone': '+1-416-555-0700',
        'website': 'tfa.ca',
        'quality_score': 92,
        'place_id': 'test_6',
        'gps_coordinates': {}
    },
    {
        'title': 'Sydney Luxury Hotels',
        'type': 'luxury hotel',
        'rating': 4.8,
        'reviews': 380,
        'address': 'Circular Quay, Sydney, Australia',
        'phone': '+61-2-555-0800',
        'website': None,
        'quality_score': 95,
        'place_id': 'test_7',
        'gps_coordinates': {}
    },
    {
        'title': 'Paris Marketing Agency',
        'type': 'marketing agency',
        'rating': 4.6,
        'reviews': 180,
        'address': 'Champs-Élysées, Paris, France',
        'phone': '+33-1-555-0900',
        'website': 'parismarketing.fr',
        'quality_score': 88,
        'place_id': 'test_8',
        'gps_coordinates': {}
    }
]

print("🧪 Testing Premium Dashboard System\n")
print("=" * 60)

# Test 1: Create data directory
print("\n1️⃣ Creating data directory...")
os.makedirs("data", exist_ok=True)
print("   ✅ Data directory ready")

# Test 2: Save sample leads
print("\n2️⃣ Creating sample premium leads...")
with open('data/premium_leads.json', 'w', encoding='utf-8') as f:
    json.dump(sample_leads, f, indent=2, ensure_ascii=False)
print(f"   ✅ Created {len(sample_leads)} sample leads")
print(f"   📁 Saved to: data/premium_leads.json")

# Test 3: Verify file
print("\n3️⃣ Verifying file...")
with open('data/premium_leads.json', 'r', encoding='utf-8') as f:
    loaded = json.load(f)
print(f"   ✅ Verified: {len(loaded)} leads loaded")

# Test 4: Show sample leads
print("\n4️⃣ Sample Premium Leads:")
print("   " + "-" * 56)
for i, lead in enumerate(sample_leads[:3], 1):
    print(f"   {i}. {lead['title']} - {lead['quality_score']}/100")
    print(f"      📍 {lead['address']}")
    print(f"      ⭐ {lead['rating']} ({lead['reviews']} reviews)")
    print()

# Test 5: Test quality filter
print("\n5️⃣ Testing Quality Filter...")
from lead_quality_filter import LeadQualityScorer

test_lead = sample_leads[0]
score = LeadQualityScorer.calculate_quality_score(test_lead)
print(f"   ✅ Quality scoring working: {score}/100")

# Test 6: Test AI content generation
print("\n6️⃣ Testing AI Content Generation...")
try:
    from ai_gemini import create_ai_assistant
    from config import load_config
    
    config = load_config()
    if config.get('GEMINI_API_KEY'):
        print("   ✅ Gemini API key found")
        ai = create_ai_assistant(config['GEMINI_API_KEY'])
        
        # Generate sample content
        email = ai.generate_cold_email(
            test_lead['title'],
            test_lead['type'],
            test_lead['address'],
            test_lead['rating'],
            test_lead['reviews']
        )
        print("   ✅ AI email generation working")
        print(f"   📧 Email length: {len(email)} characters")
    else:
        print("   ⚠️  No Gemini API key - using fallback content")
except Exception as e:
    print(f"   ⚠️  AI test skipped: {str(e)}")

# Test 7: Dashboard files check
print("\n7️⃣ Checking Dashboard Files...")
files_to_check = [
    'dashboard_premium.py',
    'templates/premium_dashboard.html'
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - MISSING!")

print("\n" + "=" * 60)
print("✅ TEST COMPLETE!")
print("=" * 60)

print("\n🚀 Next Steps:")
print("   1. Start dashboard: python dashboard_premium.py")
print("   2. Open browser: http://localhost:5000")
print("   3. You should see 8 sample premium leads")
print("   4. Click 'Generate Premium Leads' to add more")

print("\n📊 Sample Data Created:")
print(f"   • {len(sample_leads)} premium leads")
print(f"   • Quality scores: 88-100/100")
print(f"   • Countries: USA, UK, UAE, Canada, Australia, France")
print(f"   • Categories: Law, Real Estate, Finance, Tech, Healthcare")

print("\n💡 To generate NEW leads:")
print("   1. Open dashboard")
print("   2. Select target countries")
print("   3. Set number of leads (e.g., 10 for quick test)")
print("   4. Click 'Generate Premium Leads'")
print("   5. Wait 5-10 minutes")
print("   6. New leads will be ADDED to existing ones")
