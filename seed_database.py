#!/usr/bin/env python3
"""
Database Seeding Script - Pre-populate with REAL verified leads
Generates 20 leads for top cities and business types
"""

import sys
import os
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scraper import search_places
from src.lead_quality_filter import filter_serious_clients_only
from src.filters import remove_duplicates
from src.config import load_config

# Top cities to seed (5 per country)
SEED_CITIES = [
    # USA
    "New York, USA", "Los Angeles, USA", "Chicago, USA", "Houston, USA", "Miami, USA",
    # UK
    "London, UK", "Manchester, UK", "Birmingham, UK", "Edinburgh, UK", "Liverpool, UK",
    # UAE
    "Dubai, UAE", "Abu Dhabi, UAE", "Sharjah, UAE", "Ajman, UAE", "Ras Al Khaimah, UAE",
    # Canada
    "Toronto, Canada", "Vancouver, Canada", "Montreal, Canada", "Calgary, Canada", "Ottawa, Canada",
    # Australia
    "Sydney, Australia", "Melbourne, Australia", "Brisbane, Australia", "Perth, Australia", "Adelaide, Australia",
    # India
    "Mumbai, India", "Delhi, India", "Bangalore, India", "Hyderabad, India", "Chennai, India",
    # Singapore
    "Singapore",
    # Germany
    "Berlin, Germany", "Munich, Germany", "Frankfurt, Germany", "Hamburg, Germany", "Cologne, Germany",
    # France
    "Paris, France", "Lyon, France", "Marseille, France", "Nice, France", "Toulouse, France",
    # Netherlands
    "Amsterdam, Netherlands", "Rotterdam, Netherlands", "The Hague, Netherlands", "Utrecht, Netherlands",
    # Saudi Arabia
    "Riyadh, Saudi Arabia", "Jeddah, Saudi Arabia", "Mecca, Saudi Arabia", "Medina, Saudi Arabia",
]

# Top business categories to seed
SEED_CATEGORIES = [
    # High-value services
    "dental clinic",
    "law firm",
    "accounting firm",
    "real estate agency",
    "software company",
    "consulting firm",
    "medical clinic",
    "cosmetic surgery",
    "investment firm",
    "architecture firm",
    # Retail & Hospitality
    "restaurant",
    "hotel",
    "cafe",
    "gym",
    "spa",
    # Professional services
    "marketing agency",
    "web design agency",
    "photography studio",
    "event planning",
    "interior design",
]

def seed_database():
    """Seed database with real verified leads."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           DATABASE SEEDING - REAL VERIFIED LEADS         ║
    ║                                                          ║
    ║  🎯 Generating leads for top cities & categories         ║
    ║  ✅ 100% REAL data from SerpAPI                          ║
    ║  🚀 No dummy/demo data                                   ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    config = load_config()
    api_key = config.get('SERPAPI_KEY')
    
    if not api_key:
        print("❌ ERROR: SERPAPI_KEY not found in config!")
        print("Please set your SerpAPI key in src/config.py")
        return
    
    print(f"\n📊 Seeding Plan:")
    print(f"   Cities: {len(SEED_CITIES)}")
    print(f"   Categories: {len(SEED_CATEGORIES)}")
    print(f"   Target: ~{len(SEED_CITIES) * len(SEED_CATEGORIES) * 20:,} leads")
    print(f"   Estimated time: ~{len(SEED_CITIES) * len(SEED_CATEGORIES) * 2 / 60:.1f} hours")
    
    response = input("\n⚠️  This will use SerpAPI quota. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Seeding cancelled")
        return
    
    all_leads = []
    total_queries = len(SEED_CITIES) * len(SEED_CATEGORIES)
    current_query = 0
    
    print(f"\n🚀 Starting seeding process...\n")
    
    for city in SEED_CITIES:
        for category in SEED_CATEGORIES:
            current_query += 1
            query = f"{category} in {city}"
            
            print(f"[{current_query}/{total_queries}] 🔍 Searching: {query}")
            
            try:
                # Search with SerpAPI
                results = search_places(query, api_key)
                
                if not results:
                    print(f"   ⚠️  No results found")
                    continue
                
                # Filter for quality
                quality_leads = filter_serious_clients_only(results)
                premium = [lead for lead in quality_leads if lead.get('quality_score', 0) >= 70]
                
                if premium:
                    # Add metadata
                    timestamp = datetime.now().isoformat()
                    for lead in premium:
                        lead['generated_at'] = timestamp
                        lead['seed_query'] = query
                        lead['seed_city'] = city
                        lead['seed_category'] = category
                    
                    all_leads.extend(premium)
                    print(f"   ✅ Found {len(premium)} quality leads (Total: {len(all_leads)})")
                else:
                    print(f"   ⚠️  No quality leads found")
                
                # Rate limiting - be nice to SerpAPI
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                continue
    
    print(f"\n📊 Seeding Summary:")
    print(f"   Total leads found: {len(all_leads)}")
    print(f"   Queries executed: {current_query}")
    print(f"   Success rate: {len(all_leads) / current_query:.1%}")
    
    if not all_leads:
        print("\n❌ No leads to save!")
        return
    
    # Remove duplicates
    print(f"\n🔄 Removing duplicates...")
    unique_leads = remove_duplicates(all_leads)
    print(f"   Unique leads: {len(unique_leads)}")
    
    # Save to database
    print(f"\n💾 Saving to database...")
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/history", exist_ok=True)
    os.makedirs("data/backups", exist_ok=True)
    
    # Save main database
    db_path = "data/premium_leads.json"
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(unique_leads, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Saved to {db_path}")
    
    # Save to history
    today = datetime.now().strftime('%Y-%m-%d')
    history_path = f"data/history/leads_{today}.json"
    history_data = {
        'date': today,
        'timestamp': datetime.now().isoformat(),
        'total_leads': len(unique_leads),
        'leads': unique_leads,
        'seed_info': {
            'cities': len(SEED_CITIES),
            'categories': len(SEED_CATEGORIES),
            'queries': current_query
        }
    }
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Saved to {history_path}")
    
    # Create backup
    backup_path = f"data/backups/seed_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(unique_leads, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Backup saved to {backup_path}")
    
    # Generate statistics
    print(f"\n📈 Database Statistics:")
    
    # By country
    countries = {}
    for lead in unique_leads:
        address = lead.get('address', '')
        for country in ['USA', 'UK', 'UAE', 'Canada', 'Australia', 'India', 'Singapore', 'Germany', 'France', 'Netherlands', 'Saudi Arabia']:
            if country in address:
                countries[country] = countries.get(country, 0) + 1
                break
    
    print(f"\n   By Country:")
    for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
        print(f"      {country}: {count} leads")
    
    # By category
    categories = {}
    for lead in unique_leads:
        cat = lead.get('seed_category', lead.get('type', 'Unknown'))
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n   By Category (Top 10):")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"      {cat}: {count} leads")
    
    # Quality distribution
    quality_ranges = {'90-100': 0, '80-89': 0, '70-79': 0, '<70': 0}
    for lead in unique_leads:
        score = lead.get('quality_score', 0)
        if score >= 90:
            quality_ranges['90-100'] += 1
        elif score >= 80:
            quality_ranges['80-89'] += 1
        elif score >= 70:
            quality_ranges['70-79'] += 1
        else:
            quality_ranges['<70'] += 1
    
    print(f"\n   By Quality Score:")
    for range_name, count in quality_ranges.items():
        print(f"      {range_name}: {count} leads")
    
    print(f"\n✅ Database seeding complete!")
    print(f"   Total verified leads: {len(unique_leads)}")
    print(f"   Average quality score: {sum(l.get('quality_score', 0) for l in unique_leads) / len(unique_leads):.1f}/100")
    print(f"\n🚀 You can now start the dashboard and see all leads!")
    print(f"   python3 dashboard_ragspro.py")

if __name__ == '__main__':
    seed_database()
