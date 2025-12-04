"""Test AI content generation with updated RagsPro services."""

import sys
from src.ai_gemini import create_ai_assistant
from src.config import load_config

def test_ai_content():
    """Test AI content generation."""
    print("🤖 TESTING AI CONTENT GENERATION")
    print("=" * 80)
    
    # Load config
    config = load_config()
    ai = create_ai_assistant(config['GEMINI_API_KEY'])
    
    # Test business
    business = {
        'name': "Rana's Crèche",
        'type': 'Day Care Center',
        'city': 'Delhi',
        'rating': 4.9,
        'reviews': 69,
        'address': 'Ground floor, Delhi 110025, India'
    }
    
    print(f"\n📍 Test Business: {business['name']}")
    print(f"   Type: {business['type']}")
    print(f"   Rating: {business['rating']}★ ({business['reviews']} reviews)")
    print(f"   Location: {business['city']}")
    
    # Generate email
    print("\n" + "=" * 80)
    print("📧 GENERATED EMAIL:")
    print("=" * 80)
    email = ai.generate_cold_email(
        business['name'],
        business['type'],
        business['city'],
        business['rating'],
        business['reviews']
    )
    print(email)
    
    # Generate WhatsApp
    print("\n" + "=" * 80)
    print("💬 GENERATED WHATSAPP MESSAGE:")
    print("=" * 80)
    whatsapp = ai.generate_whatsapp_message(
        business['name'],
        business['type']
    )
    print(whatsapp)
    
    # Analyze business
    print("\n" + "=" * 80)
    print("🔍 BUSINESS ANALYSIS:")
    print("=" * 80)
    analysis = ai.analyze_business(
        business['name'],
        business['type'],
        business['rating'],
        business['reviews'],
        business['address']
    )
    print(analysis)
    
    print("\n" + "=" * 80)
    print("✅ AI CONTENT TEST COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    test_ai_content()
