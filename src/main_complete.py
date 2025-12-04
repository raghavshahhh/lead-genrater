"""Complete FREE Lead Generation + AI WhatsApp Auto-Chat System."""

import logging
import os
import json
from datetime import datetime
from pathlib import Path

from src.config import load_config
from src.queries import generate_queries
from src.scraper_free import search_places_free
from src.filters import is_good_lead, transform_place
from src.dedupe import load_seen_ids, save_seen_ids
from src.storage import append_to_sheet, append_to_csv
from src.ai_gemini import create_ai_assistant
from src.whatsapp_bot import create_whatsapp_bot


def setup_logging():
    """Set up logging."""
    os.makedirs("logs", exist_ok=True)
    
    log_date = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = f"logs/complete_system_{log_date}.log"
    
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


def run_complete_system():
    """Run complete system: Scraping + AI + WhatsApp Auto-Chat."""
    logger = setup_logging()
    logger.info("=" * 80)
    logger.info("🚀 COMPLETE FREE LEAD GENERATION + AI WHATSAPP SYSTEM")
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
        
        gemini_api_key = config.get("GEMINI_API_KEY")
        enable_whatsapp = config.get("ENABLE_WHATSAPP_BOT", False)
        whatsapp_auto_chat = config.get("WHATSAPP_AUTO_CHAT", False)
        
        logger.info(f"Config: MAX_LEADS={max_leads}, WhatsApp={enable_whatsapp}")
        
        # Initialize AI assistant
        ai_assistant = None
        if gemini_api_key:
            try:
                ai_assistant = create_ai_assistant(gemini_api_key)
                logger.info("✅ Gemini AI enabled")
            except Exception as e:
                logger.warning(f"Gemini AI not available: {str(e)}")
        
        # Initialize WhatsApp bot
        whatsapp_bot = None
        if enable_whatsapp and ai_assistant:
            try:
                whatsapp_bot = create_whatsapp_bot(ai_assistant)
                if whatsapp_bot.start():
                    logger.info("✅ WhatsApp Bot ready!")
                else:
                    logger.warning("WhatsApp Bot failed to start")
                    whatsapp_bot = None
            except Exception as e:
                logger.warning(f"WhatsApp Bot not available: {str(e)}")
        
        # Load processed IDs
        logger.info("Loading processed Place IDs...")
        seen_ids = load_seen_ids()
        
        # Generate queries
        logger.info("Generating search queries...")
        queries = generate_queries()
        logger.info(f"Generated {len(queries)} queries")
        
        # Scrape and collect leads
        qualified_leads = []
        new_place_ids = set()
        ai_content = []
        whatsapp_conversations = []
        
        queries_processed = 0
        total_results = 0
        filtered_out = 0
        duplicates_skipped = 0
        
        for query in queries:
            if len(qualified_leads) >= max_leads:
                logger.info(f"Reached limit ({max_leads})")
                break
            
            logger.info(f"🔍 Scraping: {query}")
            
            # FREE scraping
            places = search_places_free(query, max_results=20)
            total_results += len(places)
            queries_processed += 1
            
            # Filter and process
            for place in places:
                if len(qualified_leads) >= max_leads:
                    break
                
                if not is_good_lead(place):
                    filtered_out += 1
                    continue
                
                place_id = place.get("place_id", "")
                if place_id in seen_ids or place_id in new_place_ids:
                    duplicates_skipped += 1
                    continue
                
                # Transform lead
                lead = transform_place(place, query)
                qualified_leads.append(lead)
                new_place_ids.add(place_id)
                
                logger.info(f"✅ Lead: {lead['business_name']} ({lead['city']})")
                
                # Generate AI content
                if ai_assistant:
                    try:
                        email = ai_assistant.generate_cold_email(
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
                        
                        ai_content.append({
                            'business_name': lead['business_name'],
                            'phone': lead.get('phone', 'N/A'),
                            'email': email,
                            'whatsapp': whatsapp_msg
                        })
                        
                        logger.info(f"🤖 AI content generated")
                        
                        # Auto WhatsApp chat if enabled
                        if whatsapp_bot and whatsapp_auto_chat and lead.get('phone'):
                            phone = lead['phone'].replace('+', '').replace(' ', '').replace('-', '')
                            if phone.startswith('91') and len(phone) >= 10:
                                logger.info(f"💬 Starting auto-chat with {lead['business_name']}")
                                
                                result = whatsapp_bot.auto_conversation(
                                    phone,
                                    lead['business_name'],
                                    whatsapp_msg,
                                    max_exchanges=3
                                )
                                
                                whatsapp_conversations.append({
                                    'business_name': lead['business_name'],
                                    'phone': phone,
                                    'result': result
                                })
                                
                                if result['status'] == 'hot_lead':
                                    logger.info(f"🔥 HOT LEAD: {lead['business_name']} - {result['action']}")
                        
                    except Exception as e:
                        logger.warning(f"AI/WhatsApp error: {str(e)}")
        
        # Store leads
        logger.info(f"Storing {len(qualified_leads)} leads...")
        
        if qualified_leads:
            try:
                append_to_sheet(qualified_leads, sheet_id, service_account_file)
            except Exception as e:
                logger.error(f"Google Sheets error: {str(e)}")
            
            append_to_csv(qualified_leads)
            
            if ai_content:
                save_ai_content(ai_content)
            
            if whatsapp_conversations:
                save_whatsapp_conversations(whatsapp_conversations)
            
            if new_place_ids:
                all_ids = seen_ids | new_place_ids
                save_seen_ids(all_ids)
        
        # Close WhatsApp
        if whatsapp_bot:
            whatsapp_bot.close()
        
        # Summary
        logger.info("=" * 80)
        logger.info("📊 EXECUTION SUMMARY:")
        logger.info(f"  Queries: {queries_processed}")
        logger.info(f"  Results: {total_results}")
        logger.info(f"  Filtered: {filtered_out}")
        logger.info(f"  Duplicates: {duplicates_skipped}")
        logger.info(f"  ✅ New leads: {len(qualified_leads)}")
        if ai_content:
            logger.info(f"  🤖 AI content: {len(ai_content)}")
        if whatsapp_conversations:
            logger.info(f"  💬 WhatsApp chats: {len(whatsapp_conversations)}")
            hot_leads = sum(1 for c in whatsapp_conversations if c['result']['status'] == 'hot_lead')
            if hot_leads:
                logger.info(f"  🔥 HOT LEADS: {hot_leads}")
        logger.info("=" * 80)
        logger.info("🎉 COMPLETE SYSTEM FINISHED!")
        
        return len(qualified_leads)
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        raise


def save_ai_content(ai_content: list[dict]):
    """Save AI content to file."""
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
            f.write(f"Phone: {content['phone']}\n")
            f.write(f"{'='*80}\n\n")
            
            f.write("📧 EMAIL:\n")
            f.write("-" * 80 + "\n")
            f.write(content['email'])
            f.write("\n\n")
            
            f.write("💬 WHATSAPP:\n")
            f.write("-" * 80 + "\n")
            f.write(content['whatsapp'])
            f.write("\n\n")
    
    logging.info(f"AI content saved: {filename}")


def save_whatsapp_conversations(conversations: list[dict]):
    """Save WhatsApp conversation logs."""
    os.makedirs("data", exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"data/whatsapp_conversations_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, indent=2, ensure_ascii=False)
    
    # Also create readable text version
    txt_filename = f"data/whatsapp_conversations_{timestamp}.txt"
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("WHATSAPP AUTO-CHAT CONVERSATIONS\n")
        f.write("=" * 80 + "\n\n")
        
        for conv in conversations:
            f.write(f"\n{'='*80}\n")
            f.write(f"Business: {conv['business_name']}\n")
            f.write(f"Phone: {conv['phone']}\n")
            f.write(f"Status: {conv['result']['status']}\n")
            if 'action' in conv['result']:
                f.write(f"Action: {conv['result']['action']}\n")
            f.write(f"{'='*80}\n\n")
            
            for msg in conv['result']['conversation']:
                sender = "🤖 BOT" if msg['from'] == 'bot' else "👤 CLIENT"
                f.write(f"{sender} [{msg['time']}]:\n")
                f.write(f"{msg['message']}\n\n")
    
    logging.info(f"WhatsApp conversations saved: {txt_filename}")


if __name__ == "__main__":
    run_complete_system()
