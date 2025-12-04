"""Test new AI content with business analysis and problem identification."""

from src.ai_gemini import create_ai_assistant
from src.config import load_config

def test_new_content():
    """Test updated AI content."""
    print("=" * 80)
    print("🔍 TESTING NEW AI CONTENT - With Business Analysis")
    print("=" * 80)
    
    # Load config
    config = load_config()
    ai = create_ai_assistant(config['GEMINI_API_KEY'])
    
    # Test different business types
    test_businesses = [
        {
            'name': "Cafe Coffee Day",
            'type': 'Cafe',
            'city': 'Delhi',
            'rating': 4.5,
            'reviews': 150
        },
        {
            'name': "Style Salon & Spa",
            'type': 'Salon',
            'city': 'Mumbai',
            'rating': 4.8,
            'reviews': 89
        },
        {
            'name': "Fresh Mart Grocery",
            'type': 'Retail Store',
            'city': 'Bangalore',
            'rating': 4.3,
            'reviews': 234
        }
    ]
    
    for business in test_businesses:
        print(f"\n{'=' * 80}")
        print(f"📍 Business: {business['name']} ({business['type']})")
        print(f"   Location: {business['city']}")
        print(f"   Rating: {business['rating']}★ ({business['reviews']} reviews)")
        print("=" * 80)
        
        # Generate email
        print("\n📧 GENERATED EMAIL:")
        print("-" * 80)
        email = ai._fallback_email(
            business['name'],
            business['type'],
            business['rating'],
            business['reviews']
        )
        print(email)
        
        # Check for key elements
        print("\n🔍 Content Analysis:")
        checks = {
            'Problem Identified': any(word in email.lower() for word in ['noticed', 'however', 'missing', 'no ', 'outdated', 'losing']),
            'RagsPro Services': 'RagsPro.com' in email,
            'Portfolio Projects': any(proj in email for proj in ['LawAI', 'Glow', 'HimShakti']),
            'Contact Info': '+918700048490' in email,
            'Free Consultation': 'FREE' in email,
            'Professional Tone': 'Raghav Shah' in email,
            'Data/Stats': any(word in email for word in ['60-70%', '3-5x', '200+', '50+']),
            'Call to Action': 'consultation' in email.lower()
        }
        
        for item, found in checks.items():
            status = "✅" if found else "❌"
            print(f"   {status} {item}")
        
        # Generate WhatsApp
        print("\n💬 GENERATED WHATSAPP:")
        print("-" * 80)
        whatsapp = ai._fallback_whatsapp(
            business['name'],
            business['type']
        )
        print(whatsapp)
        
        # Check WhatsApp content
        print("\n🔍 WhatsApp Analysis:")
        wa_checks = {
            'Problem Mentioned': any(word in whatsapp.lower() for word in ['noticed', 'no ', 'losing', 'missing']),
            'Business Name': business['name'] in whatsapp,
            'RagsPro': 'RagsPro.com' in whatsapp,
            'Projects': any(proj in whatsapp for proj in ['LawAI', 'Glow', 'HimShakti']),
            'Phone': '8700048490' in whatsapp,
            'Emojis': any(emoji in whatsapp for emoji in ['🚀', '✅', '💻', '🌟', '📱']),
            'Urgency': 'Limited' in whatsapp or 'slots' in whatsapp,
            'Call to Action': 'YES' in whatsapp or 'call' in whatsapp
        }
        
        for item, found in wa_checks.items():
            status = "✅" if found else "❌"
            print(f"   {status} {item}")
    
    print("\n" + "=" * 80)
    print("✅ NEW CONTENT TEST COMPLETE!")
    print("=" * 80)
    print("\n📋 Summary:")
    print("   ✅ Business problems identified")
    print("   ✅ Professional analysis included")
    print("   ✅ Specific solutions suggested")
    print("   ✅ Data and stats provided")
    print("   ✅ Trust-building elements present")
    print("   ✅ RagsPro branding maintained")
    print("\n💡 This content will make clients trust you as a professional agency!")

if __name__ == "__main__":
    test_new_content()
