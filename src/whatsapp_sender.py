"""WhatsApp automation using pywhatkit (FREE)."""

import logging
import pywhatkit as kit
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class WhatsAppSender:
    """FREE WhatsApp sender using pywhatkit."""
    
    def __init__(self, phone_number: str = "8700048490"):
        """
        Initialize WhatsApp sender.
        
        Args:
            phone_number: Your WhatsApp number (with country code)
        """
        self.phone_number = phone_number
        logger.info(f"WhatsApp sender initialized: {phone_number}")
    
    def send_message(self, to_number: str, message: str, 
                    business_name: str = None, delay_minutes: int = 1) -> bool:
        """
        Send WhatsApp message (opens WhatsApp Web).
        
        Args:
            to_number: Recipient phone number (with country code, e.g., +919876543210)
            message: Message text
            business_name: Optional business name for logging
            delay_minutes: Minutes to wait before sending (default: 1)
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Clean phone number
            if not to_number.startswith('+'):
                # Assume Indian number if no country code
                to_number = '+91' + to_number.replace('-', '').replace(' ', '')
            
            # Get current time + delay
            now = datetime.now() + timedelta(minutes=delay_minutes)
            hour = now.hour
            minute = now.minute
            
            logger.info(f"Scheduling WhatsApp to {to_number} ({business_name or 'Unknown'}) at {hour}:{minute}")
            
            # Send message (opens WhatsApp Web)
            kit.sendwhatmsg(to_number, message, hour, minute, wait_time=15, tab_close=True)
            
            logger.info(f"WhatsApp sent to {to_number} ({business_name or 'Unknown'})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp to {to_number}: {str(e)}")
            return False
    
    def send_bulk_messages(self, recipients: list[dict], delay_between: int = 2) -> dict:
        """
        Send bulk WhatsApp messages.
        
        Args:
            recipients: List of dicts with 'phone', 'message', 'business_name' keys
            delay_between: Minutes between each message
        
        Returns:
            Dict with 'sent', 'failed', 'total' counts
        """
        results = {'sent': 0, 'failed': 0, 'total': len(recipients)}
        
        current_delay = 1  # Start with 1 minute delay
        
        for recipient in recipients:
            phone = recipient.get('phone')
            message = recipient.get('message')
            business_name = recipient.get('business_name', '')
            
            if not phone or not message:
                logger.warning(f"Skipping recipient with missing data: {business_name}")
                results['failed'] += 1
                continue
            
            # Send message
            success = self.send_message(phone, message, business_name, current_delay)
            
            if success:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            # Increment delay for next message
            current_delay += delay_between
        
        logger.info(f"Bulk WhatsApp complete: {results['sent']}/{results['total']} sent")
        return results


def create_whatsapp_sender(phone_number: str = "8700048490") -> WhatsAppSender:
    """
    Create WhatsApp sender instance.
    
    Args:
        phone_number: Your WhatsApp number
    
    Returns:
        WhatsAppSender instance
    """
    return WhatsAppSender(phone_number)
