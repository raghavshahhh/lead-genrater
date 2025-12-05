"""
🚀 FULLY AUTOMATIC LEAD GENERATION + OUTREACH
Khud se leads generate karega aur messages bhejega!
"""

import sys
import os
import logging
import time
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main automatic workflow."""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   🚀 FULLY AUTOMATIC LEAD GENERATION + OUTREACH          ║
    ║                                                          ║
    ║   Khud se leads generate karega                          ║
    ║   Khud se emails bhejega                                 ║
    ║   Khud se WhatsApp messages bhejega                      ║
    ║                                                          ║
    ║   100% AUTOMATIC - Koi manual work nahi!                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Step 1: Load configuration
        logger.info("📋 Step 1: Loading configuration...")
        from src.config import load_config
        
        config = load_config()
        
        # Check API keys
        if not config.get('GEMINI_API_KEY'):
            logger.error("❌ GEMINI_API_KEY not found in config!")
            logger.info("💡 Add it to config/settings.json")
            return
        
        if not config.get('GMAIL_ADDRESS') or not config.get('GMAIL_APP_PASSWORD'):
            logger.warning("⚠️ Gmail not configured. Emails will be skipped.")
            send_email = False
        else:
            send_email = True
        
        logger.info("✅ Configuration loaded")
        
        # Step 2: Initialize services
        logger.info("\n📋 Step 2: Initializing services...")
        
        from src.ai_gemini import create_ai_assistant
        from src.email_sender import create_gmail_sender
        from src.whatsapp_sender import create_whatsapp_sender
        from src.auto_sender import create_auto_sender
        
        ai = create_ai_assistant(config['GEMINI_API_KEY'])
        logger.info("✅ AI assistant ready")
        
        if send_email:
            gmail = create_gmail_sender(
                config['GMAIL_ADDRESS'],
                config['GMAIL_APP_PASSWORD']
            )
            logger.info("✅ Gmail sender ready")
        else:
            gmail = None
            logger.info("⚠️ Gmail sender skipped")
        
        whatsapp = create_whatsapp_sender(auto_mode=True)
        logger.info("✅ WhatsApp sender ready")
        
        # Create auto sender
        auto_sender = create_auto_sender(gmail, whatsapp, ai)
        logger.info("✅ Auto sender ready")
        
        # Step 3: Load or generate leads
        logger.info("\n📋 Step 3: Loading leads...")
        
        import json
        leads_file = "data/premium_leads.json"
        
        if os.path.exists(leads_file):
            with open(leads_file, 'r', encoding='utf-8') as f:
                leads = json.load(f)
            logger.info(f"✅ Loaded {len(leads)} existing leads")
        else:
            logger.info("⚠️ No leads found. Generating new leads...")
            
            # Generate leads
            from src.main_premium_clients import generate_premium_leads
            from src.queries import CITIES, CATEGORIES
            
            logger.info("🔍 Generating premium leads...")
            logger.info(f"📍 Cities: {len(CITIES)}")
            logger.info(f"📂 Categories: {len(CATEGORIES)}")
            
            leads = generate_premium_leads(
                target_countries=['USA', 'UK', 'UAE'],
                num_leads=50,
                quality_threshold=70
            )
            
            logger.info(f"✅ Generated {len(leads)} premium leads")
            
            # Save leads
            os.makedirs("data", exist_ok=True)
            with open(leads_file, 'w', encoding='utf-8') as f:
                json.dump(leads, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Leads saved to {leads_file}")
        
        if not leads:
            logger.error("❌ No leads available!")
            return
        
        # Step 4: Filter leads that haven't been contacted
        logger.info("\n📋 Step 4: Filtering leads...")
        
        uncontacted_leads = [
            lead for lead in leads
            if not lead.get('email_sent') and not lead.get('whatsapp_sent')
        ]
        
        logger.info(f"✅ Found {len(uncontacted_leads)} uncontacted leads")
        
        if not uncontacted_leads:
            logger.info("✅ All leads already contacted!")
            logger.info("💡 Generate new leads or wait for responses")
            return
        
        # Step 5: Ask user for confirmation
        logger.info("\n📋 Step 5: Ready to send!")
        logger.info(f"📊 Will contact {len(uncontacted_leads)} leads")
        logger.info(f"📧 Email: {'YES' if send_email else 'NO'}")
        logger.info(f"💬 WhatsApp: YES")
        logger.info(f"⏱️ Estimated time: {len(uncontacted_leads) * 0.5} minutes")
        
        response = input("\n🚀 Start automatic outreach? (yes/no): ").strip().lower()
        
        if response not in ['yes', 'y']:
            logger.info("❌ Cancelled by user")
            return
        
        # Step 6: Run automatic campaign
        logger.info("\n📋 Step 6: Starting AUTOMATIC campaign...")
        logger.info("🚀 Sit back and relax - System will do everything!")
        
        results = auto_sender.send_bulk_automatic(
            leads=uncontacted_leads[:20],  # Limit to 20 per run (safety)
            send_email=send_email,
            send_whatsapp=True,
            delay_between_leads=30,  # 30 seconds between leads
            max_per_day=20
        )
        
        # Step 7: Save updated leads
        logger.info("\n📋 Step 7: Saving results...")
        
        with open(leads_file, 'w', encoding='utf-8') as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        logger.info("✅ Leads updated")
        
        # Step 8: Show final statistics
        logger.info("\n" + "="*60)
        logger.info("🎉 CAMPAIGN COMPLETE!")
        logger.info("="*60)
        logger.info(f"📊 Total Leads: {results['total_leads']}")
        logger.info(f"✅ Processed: {results['processed']}")
        logger.info(f"📧 Emails Sent: {results['emails_sent']}")
        logger.info(f"💬 WhatsApp Sent: {results['whatsapp_sent']}")
        logger.info(f"❌ Failed: {results['emails_failed'] + results['whatsapp_failed']}")
        logger.info("="*60)
        
        # Save campaign report
        report_file = f"data/campaign_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Report saved: {report_file}")
        
        logger.info("\n✅ ALL DONE! Check your Gmail and WhatsApp for sent messages.")
        logger.info("💰 Now wait for responses and book calls!")
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"\n❌ Error: {str(e)}", exc_info=True)
        logger.info("💡 Check the error and try again")


if __name__ == '__main__':
    main()
