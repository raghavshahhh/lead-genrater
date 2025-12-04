"""Main orchestrator for FREE Lead Generation Bot with AI."""

import logging
import os
from datetime import datetime
from pathlib import Path

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import load_config
from src.queries import generate_queries
from src.scraper import search_places  # REAL SerpAPI scraper
from src.filters import is_good_lead, transform_place
from src.dedupe import load_seen_ids, save_seen_ids
from src.storage import append_to_sheet, append_to_csv
from src.ai_gemini import create_ai_assistant
from src.email_sender import create_gmail_sender


def setup_logging():
    """Set up logging with ISO 8601 timestamps and daily log files."""
    os.makedirs("logs", exist_ok=True)
    
    log_date = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = f"logs/lead_bot_free_{log_date}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def run_free():
    """Execute the FREE lead generation workflow with AI."""
    logger = setup_logging()
    logger.info("=" * 80)
    logger.info("Starting FREE Lead Generation Bot with AI")
    logger.info("=" * 80)
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        
        sheet_id = config.get("GOOGLE_SHEET_ID")
        service_account_file = config.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        min_rating = config.get("MIN_RATING", 4.0)
        min_reviews = config.get("MIN_REVIEWS", 20)
        max_leads = config.get("MAX_LEADS_PER_RUN", 50)
        
        # Optional: AI and Email (can work without these)
        gemini_api_key = config.get("GEMINI_API_KEY")
        gmail_address = config.get("GMAIL_ADDRESS")
        gmail_app_password = config.get("GMAIL_APP_PASSWORD")
        
        logger.info(f"Configuration: MAX_LEADS={max_leads}, MIN_RATING={min_rating}, MIN_REVIEWS={min_reviews}")
        
        # Initialize AI assistant (optional)
        ai_assistant = None
        if gemini_api_key:
            try:
                ai_assistant = create_ai_assistant(gemini_api_key)
                logger.info("✅ Gemini AI enabled (FREE)")
            except Exception as e:
                logger.warning(f"Gemini AI not available: {str(e)}")
        
        # Initialize email sender (optional)
        email_sender = None
        if gmail_address and gmail_app_password:
            try:
                email_sender = create_gmail_sender(gmail_address, gmail_app_password)
                logger.info("✅ Gmail sender enabled (FREE - 500/day)")
            except Exception as e:
                logger.warning(f"Gmail sender not available: {str(e)}")
        
        # Load previously processed Place IDs
        logger.info("Loading processed Place IDs...")
        seen_ids = load_seen_ids()
        logger.info(f"Loaded {len(seen_ids)} previously processed Place IDs")
        
        # Generate queries
        logger.info("Generating search queries...")
        queries = generate_queries()
        logger.info(f"Generated {len(queries)} search queries")
        
        # Process queries and collect leads
        qualified_leads = []
        new_place_ids = set()
        ai_generated_content = []
        
        queries_processed = 0
        total_results = 0
        filtered_out = 0
        duplicates_skipped = 0
        
        for query in queries:
            # Check if we've reached the limit
            if len(qualified_leads) >= max_leads:
                logger.info(f"Reached maximum lead limit ({max_leads}). Stopping.")
                break
            
            logger.info(f"🔍 REAL Scraping with SerpAPI: {query}")
            
            # REAL scraping with SerpAPI
            serpapi_key = config.get('SERPAPI_KEY')
            if not serpapi_key:
                logger.error("SERPAPI_KEY not found in config!")
                break
            
            places = search_places(query, serpapi_key)
            total_results += len(places)
            queries_processed += 1
            
            # Filter and transform
            for place in places:
                if len(qualified_leads) >= max_leads:
                    break
                
                # Check if it's a good lead
                if not is_good_lead(place):
                    filtered_out += 1
                    continue
                
                # Check for duplicates
                place_id = place.get("place_id", "")
                if place_id in seen_ids or place_id in new_place_ids:
                    duplicates_skipped += 1
                    logger.debug(f"Skipping duplicate: {place_id}")
                    continue
                
                # Transform and add to qualified leads
                lead = transform_place(place, query)
                qualified_leads.append(lead)
                new_place_ids.add(place_id)
                
                logger.info(f"✅ Qualified: {lead['business_name']} ({lead['city']})")
                
                # Generate AI content if available
                if ai_assistant:
                    try:
                        email_content = ai_assistant.generate_cold_email(
                            lead['business_name'],
                            lead['category'],
                            lead['city'],
                            lead['rating'],
                            lead['reviews_count']
                        )
                        
                        whatsapp_msg = ai_assistant.generate_whatsapp_message(
                            lead['business_name'],
                            lead['category']
                        )
                        
                        ai_generated_content.append({
                            'business_name': lead['business_name'],
                            'email': email_content,
                            'whatsapp': whatsapp_msg
                        })
                        
                        logger.info(f"🤖 AI content generated for {lead['business_name']}")
                    except Exception as e:
                        logger.warning(f"AI generation failed: {str(e)}")
        
        # Store leads
        logger.info(f"Storing {len(qualified_leads)} qualified leads...")
        
        if qualified_leads:
            # Store to Google Sheets
            try:
                append_to_sheet(qualified_leads, sheet_id, service_account_file)
            except Exception as e:
                logger.error(f"Failed to store to Google Sheets: {str(e)}")
            
            # Store to CSV
            append_to_csv(qualified_leads)
            
            # Save AI generated content
            if ai_generated_content:
                save_ai_content(ai_generated_content)
            
            # Save new Place IDs
            if new_place_ids:
                all_ids = seen_ids | new_place_ids
                save_seen_ids(all_ids)
        
        # Log execution summary
        logger.info("=" * 80)
        logger.info("📊 Execution Summary:")
        logger.info(f"  Queries processed: {queries_processed}")
        logger.info(f"  Total results found: {total_results}")
        logger.info(f"  Leads filtered out: {filtered_out}")
        logger.info(f"  Duplicates skipped: {duplicates_skipped}")
        logger.info(f"  ✅ New leads added: {len(qualified_leads)}")
        if ai_generated_content:
            logger.info(f"  🤖 AI content generated: {len(ai_generated_content)}")
        logger.info("=" * 80)
        logger.info("🎉 FREE Lead Generation Bot completed successfully!")
        
        return len(qualified_leads)
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        raise


def save_ai_content(ai_content: list[dict]):
    """Save AI-generated content to file for manual use."""
    os.makedirs("data", exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"data/ai_content_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("AI-GENERATED CONTENT FOR OUTREACH\n")
        f.write("=" * 80 + "\n\n")
        
        for idx, content in enumerate(ai_content, 1):
            f.write(f"\n{'='*80}\n")
            f.write(f"LEAD #{idx}: {content['business_name']}\n")
            f.write(f"{'='*80}\n\n")
            
            f.write("📧 EMAIL:\n")
            f.write("-" * 80 + "\n")
            f.write(content['email'])
            f.write("\n\n")
            
            f.write("💬 WHATSAPP:\n")
            f.write("-" * 80 + "\n")
            f.write(content['whatsapp'])
            f.write("\n\n")
    
    logging.info(f"AI content saved to: {filename}")


if __name__ == "__main__":
    run_free()
