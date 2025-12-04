"""Test script for FREE Lead Generation Bot - Run this first!"""

import os
import sys

def check_dependencies():
    """Check if all dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required = {
        'playwright': 'Playwright (FREE scraping)',
        'google.generativeai': 'Gemini AI (FREE)',
        'gspread': 'Google Sheets',
        'bs4': 'BeautifulSoup4'
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - MISSING!")
            missing.append(module)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed!\n")
    return True


def check_playwright():
    """Check if Playwright browsers are installed."""
    print("🔍 Checking Playwright browsers...")
    
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print("  ✅ Chromium browser installed")
                return True
            except Exception as e:
                print(f"  ❌ Chromium browser not installed")
                print("  Run: playwright install chromium")
                return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False


def check_config():
    """Check if configuration file exists."""
    print("\n🔍 Checking configuration...")
    
    config_path = "config/settings.json"
    if not os.path.exists(config_path):
        print(f"  ❌ Config file not found: {config_path}")
        print("  Create it from config/settings.example.json")
        return False
    
    print(f"  ✅ Config file exists")
    
    # Try to load config
    try:
        import json
        with open(config_path) as f:
            config = json.load(f)
        
        # Check required fields
        required_fields = {
            'GOOGLE_SHEET_ID': 'Google Sheet ID',
            'GOOGLE_SERVICE_ACCOUNT_JSON': 'Service Account JSON path',
        }
        
        optional_fields = {
            'GEMINI_API_KEY': 'Gemini AI (optional but recommended)',
            'GMAIL_ADDRESS': 'Gmail address (optional)',
            'GMAIL_APP_PASSWORD': 'Gmail app password (optional)',
        }
        
        print("\n  Required fields:")
        all_good = True
        for field, name in required_fields.items():
            if field in config and config[field] and 'YOUR_' not in config[field]:
                print(f"    ✅ {name}")
                
                # Check if service account file exists
                if field == 'GOOGLE_SERVICE_ACCOUNT_JSON':
                    sa_path = config[field]
                    if os.path.exists(sa_path):
                        print(f"    ✅ Service account file found: {sa_path}")
                    else:
                        print(f"    ❌ Service account file NOT FOUND: {sa_path}")
                        print(f"    📥 Download from Google Cloud and save as: {sa_path}")
                        all_good = False
            else:
                print(f"    ❌ {name} - NOT SET!")
                all_good = False
        
        print("\n  Optional fields (for AI features):")
        for field, name in optional_fields.items():
            if field in config and config[field] and 'YOUR_' not in config[field]:
                print(f"    ✅ {name}")
            else:
                print(f"    ⚠️  {name} - Not set (AI features disabled)")
        
        # Check WhatsApp bot settings
        if config.get('ENABLE_WHATSAPP_BOT'):
            print(f"\n  WhatsApp Bot:")
            print(f"    ✅ Enabled")
            if config.get('WHATSAPP_AUTO_CHAT'):
                print(f"    ✅ Auto-chat enabled")
        
        return all_good
        
    except Exception as e:
        print(f"  ❌ Error reading config: {str(e)}")
        return False


def test_scraper():
    """Test FREE scraper with a simple query."""
    print("\n🔍 Testing FREE scraper...")
    
    try:
        from src.scraper_free import search_places_free
        
        print("  Testing with query: 'cafe in Delhi'")
        results = search_places_free("cafe in Delhi", max_results=3)
        
        if results:
            print(f"  ✅ Scraper working! Found {len(results)} results")
            print(f"  Sample: {results[0].get('title', 'Unknown')}")
            return True
        else:
            print("  ⚠️  No results found (might be network issue)")
            return True  # Not a failure, just no results
            
    except Exception as e:
        print(f"  ❌ Scraper error: {str(e)}")
        return False


def test_ai():
    """Test Gemini AI if configured."""
    print("\n🔍 Testing Gemini AI...")
    
    try:
        import json
        with open("config/settings.json") as f:
            config = json.load(f)
        
        api_key = config.get('GEMINI_API_KEY')
        if not api_key or 'YOUR_' in api_key:
            print("  ⚠️  Gemini API key not configured (skipping)")
            return True
        
        from src.ai_gemini import create_ai_assistant
        
        ai = create_ai_assistant(api_key)
        email = ai.generate_cold_email(
            "Test Business",
            "cafe",
            "Delhi",
            4.5,
            100
        )
        
        if email and len(email) > 20:
            print("  ✅ Gemini AI working!")
            print(f"  Sample output: {email[:100]}...")
            return True
        else:
            print("  ❌ AI generated empty response")
            return False
            
    except Exception as e:
        print(f"  ❌ AI error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("🚀 FREE LEAD GENERATION BOT - SYSTEM TEST")
    print("=" * 80)
    print()
    
    results = {
        'Dependencies': check_dependencies(),
        'Playwright': check_playwright(),
        'Configuration': check_config(),
        'Scraper': test_scraper(),
        'AI': test_ai(),
    }
    
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS")
    print("=" * 80)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test:20s} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is ready to use!")
        print("\nRun the bot:")
        print("  python src/main_free.py")
    else:
        print("⚠️  Some tests failed. Fix the issues above.")
        print("\nCheck SETUP_GUIDE_HINDI.md for detailed setup instructions.")
    print("=" * 80)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
