"""
PREMIUM CLIENT LEAD GENERATOR
Finds HIGH-PAYING, SERIOUS international clients using FREE scraping.

Features:
✅ International cities (USA, UK, Dubai, Canada, Australia, Europe)
✅ High-value businesses (Law firms, Finance, Real Estate, Tech, Healthcare)
✅ Quality filtering (Only serious clients with high budgets)
✅ FREE unlimited scraping (No API costs)
✅ AI-powered personalized outreach
"""

import logging
from typing import List, Dict
import sys

# Import our modules
from scraper_free_unlimited import search_places_free
from lead_quality_filter import filter_serious_clients_only
from queries import generate_queries, CITIES, CATEGORIES
from storage import save_leads, load_existing_leads
from filters import remove_duplicates

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_premium_leads(
    max_leads: int = 100,
    min_quality_score: float = 70.0,
    target_countries: List[str] = None
) -> List[Dict]:
    """
    Generate premium quality leads from international markets.
    
    Args:
        max_leads: Maximum number of leads to generate
        min_quality_score: Minimum quality score (0-100)
        target_countries: List of countries to target (e.g., ['USA', 'UK', 'UAE'])
        
    Returns:
        List of premium quality leads
    """
    logger.info("🚀 Starting PREMIUM CLIENT Lead Generation")
    logger.info(f"Target: {max_leads} HIGH-PAYING, SERIOUS clients")
    logger.info(f"Quality threshold: {min_quality_score}/100")
    
    # Filter cities by target countries if specified
    if target_countries:
        filtered_cities = [city for city in CITIES 
                          if any(country in city for country in target_countries)]
        logger.info(f"Targeting {len(filtered_cities)} cities in: {', '.join(target_countries)}")
    else:
        filtered_cities = CITIES
        logger.info(f"Targeting {len(filtered_cities)} international cities")
    
    # Generate queries (prioritize high-value categories)
    all_queries = []
    for city in filtered_cities:
        for category in CATEGORIES[:20]:  # Top 20 highest-paying categories
            query = f"{category} in {city}"
            all_queries.append(query)
    
    logger.info(f"Generated {len(all_queries)} search queries")
    
    # Scrape leads
    all_leads = []
    premium_leads = []
    
    for i, query in enumerate(all_queries):
        if len(premium_leads) >= max_leads:
            logger.info(f"✅ Reached target of {max_leads} premium leads!")
            break
        
        logger.info(f"\n[{i+1}/{len(all_queries)}] Searching: {query}")
        
        try:
            # FREE scraping
            results = search_places_free(query, max_results=10)
            
            if not results:
                logger.warning(f"No results for: {query}")
                continue
            
            all_leads.extend(results)
            
            # Filter for quality
            quality_leads = filter_serious_clients_only(results)
            
            # Further filter by minimum score
            premium = [lead for lead in quality_leads 
                      if lead.get('quality_score', 0) >= min_quality_score]
            
            if premium:
                premium_leads.extend(premium)
                logger.info(f"✅ Found {len(premium)} PREMIUM leads (Total: {len(premium_leads)})")
            
        except Exception as e:
            logger.error(f"Error scraping {query}: {str(e)}")
            continue
    
    # Remove duplicates
    logger.info("\n🔄 Removing duplicates...")
    unique_leads = remove_duplicates(premium_leads)
    
    logger.info(f"\n✅ FINAL RESULTS:")
    logger.info(f"   Total scraped: {len(all_leads)}")
    logger.info(f"   Premium quality: {len(premium_leads)}")
    logger.info(f"   After deduplication: {len(unique_leads)}")
    
    # Show top 5 leads
    if unique_leads:
        logger.info(f"\n🏆 TOP 5 PREMIUM LEADS:")
        for i, lead in enumerate(unique_leads[:5], 1):
            logger.info(f"   {i}. {lead['title']} - Score: {lead.get('quality_score', 0):.0f}/100")
            logger.info(f"      Type: {lead.get('type', 'N/A')}")
            logger.info(f"      Location: {lead.get('address', 'N/A')}")
            logger.info(f"      Rating: {lead.get('rating', 0)} ({lead.get('reviews', 0)} reviews)")
    
    return unique_leads


def main():
    """Main function to run premium lead generation."""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     PREMIUM CLIENT LEAD GENERATOR - RagsPro.com          ║
    ║                                                          ║
    ║  🎯 HIGH-PAYING International Clients                    ║
    ║  💰 Serious Businesses Only                              ║
    ║  🆓 100% FREE Scraping                                   ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Configuration
    print("\n📋 Configuration:")
    print("1. Target ALL international markets (USA, UK, UAE, Canada, Australia, Europe)")
    print("2. Target specific countries only")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    target_countries = None
    if choice == "2":
        print("\nAvailable countries:")
        print("USA, UK, UAE, Canada, Australia, France, Germany, Netherlands,")
        print("Switzerland, Sweden, Denmark, Norway, Ireland, Qatar, Saudi Arabia,")
        print("Hong Kong, Singapore, Japan, South Korea, India")
        
        countries_input = input("\nEnter countries (comma-separated): ").strip()
        target_countries = [c.strip() for c in countries_input.split(',')]
        print(f"✅ Targeting: {', '.join(target_countries)}")
    
    max_leads = int(input("\nHow many premium leads do you want? (default: 50): ").strip() or "50")
    min_score = float(input("Minimum quality score (0-100, default: 70): ").strip() or "70")
    
    print(f"\n🚀 Starting lead generation...")
    print(f"   Target: {max_leads} leads")
    print(f"   Quality threshold: {min_score}/100")
    
    # Generate leads
    try:
        leads = generate_premium_leads(
            max_leads=max_leads,
            min_quality_score=min_score,
            target_countries=target_countries
        )
        
        if leads:
            # Save to file
            print(f"\n💾 Saving {len(leads)} premium leads...")
            save_leads(leads, filename='data/premium_leads.json')
            
            print(f"\n✅ SUCCESS! Generated {len(leads)} PREMIUM leads")
            print(f"📁 Saved to: data/premium_leads.json")
            
            # Show summary
            print(f"\n📊 SUMMARY:")
            avg_score = sum(l.get('quality_score', 0) for l in leads) / len(leads)
            print(f"   Average quality score: {avg_score:.1f}/100")
            
            # Count by country
            countries = {}
            for lead in leads:
                address = lead.get('address', '')
                for country in ['USA', 'UK', 'UAE', 'Canada', 'Australia', 'France', 'Germany']:
                    if country in address:
                        countries[country] = countries.get(country, 0) + 1
                        break
            
            print(f"\n🌍 Leads by country:")
            for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
                print(f"   {country}: {count} leads")
            
            print(f"\n🎯 Next steps:")
            print(f"   1. Review leads in: data/premium_leads.json")
            print(f"   2. Run dashboard: python dashboard.py")
            print(f"   3. Generate AI content: python src/ai_gemini.py")
            print(f"   4. Start outreach via WhatsApp/Email")
            
        else:
            print("\n❌ No premium leads found. Try:")
            print("   - Lowering quality threshold")
            print("   - Targeting more cities")
            print("   - Checking internet connection")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
