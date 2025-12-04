"""
Quick Test - Generate 5 real premium leads
Tests the complete system end-to-end
"""

import sys
sys.path.insert(0, 'src')

print("""
╔══════════════════════════════════════════════════════════╗
║     QUICK GENERATION TEST - 5 Premium Leads             ║
╚══════════════════════════════════════════════════════════╝
""")

print("🧪 Testing complete premium lead generation system...")
print("   This will generate 5 REAL premium leads")
print("   Target: USA only (fastest)")
print("   Quality: 70/100")
print()

try:
    from main_premium_clients import generate_premium_leads
    
    print("🚀 Starting generation...")
    print("   (This may take 2-3 minutes)")
    print()
    
    # Generate 5 leads from USA only
    leads = generate_premium_leads(
        max_leads=5,
        min_quality_score=70,
        target_countries=['USA']
    )
    
    print()
    print("=" * 60)
    print(f"✅ SUCCESS! Generated {len(leads)} premium leads")
    print("=" * 60)
    
    if leads:
        print("\n🏆 Premium Leads Generated:")
        for i, lead in enumerate(leads, 1):
            print(f"\n{i}. {lead['title']}")
            print(f"   Type: {lead.get('type', 'N/A')}")
            print(f"   Location: {lead.get('address', 'N/A')}")
            print(f"   Quality Score: {lead.get('quality_score', 0)}/100")
            print(f"   Rating: {lead.get('rating', 0)}⭐ ({lead.get('reviews', 0)} reviews)")
            print(f"   Phone: {lead.get('phone', 'N/A')}")
            print(f"   Website: {lead.get('website') or 'None (Opportunity!)'}")
        
        print("\n" + "=" * 60)
        print("📁 Leads saved to: data/premium_leads.json")
        print()
        print("🚀 Next Steps:")
        print("   1. Start dashboard: python dashboard_premium.py")
        print("   2. Open browser: http://localhost:5000")
        print("   3. You'll see these leads + sample leads")
        print("   4. Generate more from dashboard!")
        
    else:
        print("\n⚠️  No leads generated")
        print("   Possible reasons:")
        print("   - Internet connection issue")
        print("   - Scraping methods failed")
        print("   - Quality threshold too high")
        print()
        print("   Try:")
        print("   - Check internet connection")
        print("   - Install Selenium: pip install selenium webdriver-manager")
        print("   - Lower quality threshold to 60")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print()
    print("Troubleshooting:")
    print("   1. Check internet connection")
    print("   2. Install dependencies: pip install -r requirements.txt")
    print("   3. Install Selenium: pip install selenium webdriver-manager")
    
    import traceback
    print("\nFull error:")
    traceback.print_exc()
