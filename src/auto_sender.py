"""
FULLY AUTOMATIC SENDER - Gmail + WhatsApp
Khud se messages bhejega, koi manual work nahi!
"""

import logging
import time
from datetime import datetime
from typing import List, Dict
import json
import os

logger = logging.getLogger(__name__)


class AutoSender:
    """Fully automatic sender for Gmail + WhatsApp."""
    
    def __init__(self, gmail_sender, whatsapp_sender, ai_assistant):
        """
        Initialize auto sender.
        
        Args:
            gmail_sender: GmailSender instance
            whatsapp_sender: WhatsAppSender instance
            ai_assistant: GeminiAI instance
        """
        self.gmail = gmail_sender
        self.whatsapp = whatsapp_sender
        self.ai = ai_assistant
        self.stats = {
            'emails_sent': 0,
            'emails_failed': 0,
            'whatsapp_sent': 0,
            'whatsapp_failed': 0,
            'total_processed': 0
        }
        logger.info("🚀 Auto Sender initialized - Ready for automatic outreach!")
    
    def send_to_lead(self, lead: Dict, send_email: bool = True, 
                     send_whatsapp: bool = True, delay: int = 3) -> Dict:
        """
        Automatically send email AND WhatsApp to a single lead.
        
        Args:
            lead: Lead dictionary with business info
            send_email: Whether to send email (default: True)
            send_whatsapp: Whether to send WhatsApp (default: True)
            delay: Delay between email and WhatsApp (seconds)
        
        Returns:
            Dict with results
        """
        business_name = lead.get('title', 'Business Owner')
        results = {
            'business_name': business_name,
            'email_sent': False,
            'whatsapp_sent': False,
            'errors': []
        }
        
        logger.info(f"📤 Auto-sending to: {business_name}")
        
        # Generate AI content
        try:
            email_content = self.ai.generate_cold_email(
                business_name=business_name,
                business_type=lead.get('type', 'business'),
                city=lead.get('address', ''),
                rating=lead.get('rating', 0),
                reviews=lead.get('reviews', 0)
            )
            
            whatsapp_content = self.ai.generate_whatsapp_message(
                business_name=business_name,
                business_type=lead.get('type', 'business')
            )
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            results['errors'].append(f"AI generation failed: {str(e)}")
            return results
        
        # Send Email (if enabled and email exists)
        if send_email:
            email = lead.get('email', '')
            if not email:
                # Try to construct email from business name
                email = self._guess_email(business_name, lead.get('website', ''))
            
            if email:
                try:
                    subject = f"Quick question about {business_name}'s growth"
                    success = self.gmail.send_email(
                        to_email=email,
                        subject=subject,
                        body=email_content,
                        business_name=business_name
                    )
                    
                    if success:
                        results['email_sent'] = True
                        self.stats['emails_sent'] += 1
                        logger.info(f"✅ Email sent to {business_name}")
                    else:
                        self.stats['emails_failed'] += 1
                        results['errors'].append("Email send failed")
                        
                except Exception as e:
                    logger.error(f"Email error: {e}")
                    self.stats['emails_failed'] += 1
                    results['errors'].append(f"Email error: {str(e)}")
            else:
                results['errors'].append("No email address found")
        
        # Delay between email and WhatsApp
        if send_email and send_whatsapp and delay > 0:
            time.sleep(delay)
        
        # Send WhatsApp (if enabled and phone exists)
        if send_whatsapp:
            phone = lead.get('phone', '')
            if phone:
                try:
                    success = self.whatsapp.send_message(
                        phone_number=phone,
                        message=whatsapp_content,
                        business_name=business_name
                    )
                    
                    if success:
                        results['whatsapp_sent'] = True
                        self.stats['whatsapp_sent'] += 1
                        logger.info(f"✅ WhatsApp sent to {business_name}")
                    else:
                        self.stats['whatsapp_failed'] += 1
                        results['errors'].append("WhatsApp send failed")
                        
                except Exception as e:
                    logger.error(f"WhatsApp error: {e}")
                    self.stats['whatsapp_failed'] += 1
                    results['errors'].append(f"WhatsApp error: {str(e)}")
            else:
                results['errors'].append("No phone number found")
        
        self.stats['total_processed'] += 1
        return results
    
    def send_bulk_automatic(self, leads: List[Dict], 
                           send_email: bool = True,
                           send_whatsapp: bool = True,
                           delay_between_leads: int = 30,
                           max_per_day: int = 50) -> Dict:
        """
        Fully automatic bulk sending to multiple leads.
        
        Args:
            leads: List of lead dictionaries
            send_email: Whether to send emails
            send_whatsapp: Whether to send WhatsApp
            delay_between_leads: Delay between each lead (seconds)
            max_per_day: Maximum leads to process per day
        
        Returns:
            Dict with complete statistics
        """
        logger.info(f"🚀 Starting AUTOMATIC bulk campaign for {len(leads)} leads")
        logger.info(f"📧 Email: {send_email} | 💬 WhatsApp: {send_whatsapp}")
        
        results = []
        processed = 0
        
        for i, lead in enumerate(leads):
            if processed >= max_per_day:
                logger.info(f"⚠️ Reached daily limit of {max_per_day} leads")
                break
            
            try:
                logger.info(f"\n[{i+1}/{len(leads)}] Processing: {lead.get('title', 'Unknown')}")
                
                result = self.send_to_lead(
                    lead=lead,
                    send_email=send_email,
                    send_whatsapp=send_whatsapp,
                    delay=3
                )
                
                results.append(result)
                processed += 1
                
                # Update lead status
                lead['status'] = 'Contacted'
                lead['last_contacted'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if result['email_sent']:
                    lead['email_sent'] = True
                if result['whatsapp_sent']:
                    lead['whatsapp_sent'] = True
                
                # Delay between leads (anti-spam)
                if i < len(leads) - 1:
                    logger.info(f"⏳ Waiting {delay_between_leads}s before next lead...")
                    time.sleep(delay_between_leads)
                    
            except Exception as e:
                logger.error(f"Error processing lead: {e}")
                results.append({
                    'business_name': lead.get('title', 'Unknown'),
                    'email_sent': False,
                    'whatsapp_sent': False,
                    'errors': [str(e)]
                })
        
        # Final statistics
        summary = {
            'total_leads': len(leads),
            'processed': processed,
            'emails_sent': self.stats['emails_sent'],
            'emails_failed': self.stats['emails_failed'],
            'whatsapp_sent': self.stats['whatsapp_sent'],
            'whatsapp_failed': self.stats['whatsapp_failed'],
            'results': results
        }
        
        logger.info(f"\n✅ CAMPAIGN COMPLETE!")
        logger.info(f"📊 Processed: {processed}/{len(leads)}")
        logger.info(f"📧 Emails: {self.stats['emails_sent']} sent, {self.stats['emails_failed']} failed")
        logger.info(f"💬 WhatsApp: {self.stats['whatsapp_sent']} sent, {self.stats['whatsapp_failed']} failed")
        
        return summary
    
    def _guess_email(self, business_name: str, website: str = '') -> str:
        """
        Try to guess email from business name or website.
        
        Args:
            business_name: Name of business
            website: Website URL (optional)
        
        Returns:
            Guessed email or empty string
        """
        if website:
            # Extract domain from website
            domain = website.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
            
            # Common email patterns
            patterns = [
                f"info@{domain}",
                f"contact@{domain}",
                f"hello@{domain}",
                f"sales@{domain}"
            ]
            
            # Return first pattern (most common)
            return patterns[0]
        
        return ''
    
    def get_stats(self) -> Dict:
        """Get current statistics."""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset statistics."""
        self.stats = {
            'emails_sent': 0,
            'emails_failed': 0,
            'whatsapp_sent': 0,
            'whatsapp_failed': 0,
            'total_processed': 0
        }
        logger.info("📊 Statistics reset")


def create_auto_sender(gmail_sender, whatsapp_sender, ai_assistant) -> AutoSender:
    """
    Create AutoSender instance.
    
    Args:
        gmail_sender: GmailSender instance
        whatsapp_sender: WhatsAppSender instance
        ai_assistant: GeminiAI instance
    
    Returns:
        AutoSender instance
    """
    return AutoSender(gmail_sender, whatsapp_sender, ai_assistant)
