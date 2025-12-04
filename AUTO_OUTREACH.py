"""Automatic outreach to all leads - Email + WhatsApp."""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import load_config
from src.ai_gemini import create_ai_assistant
from src.email_sender import create_gmail_sender
import csv

print("🚀 AUTOMATIC OUTREACH SYSTEM")
print("=" * 80)
print("📧 Sending personalized emails")
print("💬 Generating WhatsApp messages")
print("🎯 Target: All leads in database")
print("=" * 80)
print()

# Load config
config = load_config()

# Initialize AI
print("🤖 Initializing Gemini AI...")
ai = create_ai_assistant(config['GEMINI_API_KEY'])
print("✅ AI Ready")
print()

# Initialize email sender
print("📧 Initializing Gmail...")
email_sender = create_gmail_sender(
    config['GMAIL_ADDRESS'],
    config['GMAIL_APP_PASSWORD']
)
print("✅ Gmail Ready")
print()

# Read leads
print("📊 Reading leads from CSV...")
leads = []
with open('data/all_leads.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        leads.append(row)

print(f"✅ Found {len(leads)} leads")
print()

# Process each lead
print("🎯 Starting outreach...")
print("=" * 80)

success_count = 0
email_count = 0
whatsapp_count = 0

for idx, lead in enumerate(leads, 1):
    print(f"\n[{idx}/{len(leads)}] Processing: {lead['business_name']}")
    print(f"   City: {lead['city']}")
    print(f"   Rating: {lead['rating']}★ ({lead['reviews_count']} reviews)")
    
    try:
        # Generate email content
        print("   📧 Generating email...")
        email_content = ai.generate_cold_email(
            lead['business_name'],
            lead['category'],
            lead['city'],
            float(lead['rating']),
            int(lead['reviews_count'])
        )
        
        # Generate WhatsApp content
        print("   💬 Generating WhatsApp message...")
        whatsapp_content = ai.generate_whatsapp_message(
            lead['business_name'],
            lead['category']
        )
        
        # Save to file for manual sending
        # (Since we don't have email addresses in leads)
        with open(f'data/outreach_{lead["place_id"]}.txt', 'w', encoding='utf-8') as f:
            f.write(f"BUSINESS: {lead['business_name']}\n")
            f.write(f"PHONE: {lead['phone']}\n")
            f.write(f"CITY: {lead['city']}\n")
            f.write(f"RATING: {lead['rating']}★\n")
            f.write("\n" + "=" * 80 + "\n")
            f.write("EMAIL CONTENT:\n")
            f.write("=" * 80 + "\n")
            f.write(email_content)
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("WHATSAPP MESSAGE:\n")
            f.write("=" * 80 + "\n")
            f.write(whatsapp_content)
            f.write("\n\n" + "=" * 80 + "\n")
            f.write(f"CONTACT INFO:\n")
            f.write(f"From: Raghav - RagsPro.com\n")
            f.write(f"Phone: 8700048490\n")
            f.write(f"Email: ragsproai@gmail.com\n")
            f.write(f"Website: ragspro.com\n")
        
        print(f"   ✅ Content saved to: data/outreach_{lead['place_id']}.txt")
        
        success_count += 1
        email_count += 1
        whatsapp_count += 1
        
        # Rate limiting
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print()
print("=" * 80)
print("📊 OUTREACH COMPLETE!")
print("=" * 80)
print(f"✅ Processed: {success_count}/{len(leads)} leads")
print(f"📧 Emails generated: {email_count}")
print(f"💬 WhatsApp messages generated: {whatsapp_count}")
print()
print("📁 All content saved in: data/outreach_*.txt")
print()
print("🎯 NEXT STEPS:")
print("1. Check data/ folder for outreach files")
print("2. Copy WhatsApp messages and send manually")
print("3. Or use WhatsApp Business API for automation")
print()
print("💡 TIP: For full automation, integrate:")
print("   - WhatsApp Business API")
print("   - Email finder API (Hunter.io)")
print("   - CRM integration")
print()
print("🎉 Happy Outreach!")
