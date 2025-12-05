"""FULLY AUTOMATIC WhatsApp sender using pywhatkit."""

import logging
import pywhatkit as kit
import time
from datetime import datetime, timedelta
import webbrowser
import urllib.parse

logger = logging.getLogger(__name__)


class WhatsAppSender:
    """FULLY AUTOMATIC WhatsApp sender - Khud se message bhejega!"""
    
    def __init__(self, phone_number: str = "8700048490", auto_mode: bool = True):
        """
        Initialize WhatsApp sender.
        
        Args:
            phone_number: Your WhatsApp number (with country code)
            auto_mode: If True, sends automatically. If False, opens WhatsApp Web.
        """
        self.phone_number = phone_number
        self.auto_mode = auto_mode
        logger.info(f"🚀 WhatsApp sender initialized (Auto Mode: {auto_mode})")
    
    def send_message(self, to_number: str, message: str, 
                    business_name: str = None, instant: bool = True) -> bool:
        """
        Send WhatsApp message AUTOMATICALLY - No manual work!
        
        Args:
            to_number: Recipient phone number (with country code, e.g., +919876543210)
            message: Message text
            business_name: Optional business name for logging
            instant: If True, sends instantly. If False, schedules for 2 min later.
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Clean phone number
            if not to_number.startswith('+'):
                # Assume Indian number if no country code
                to_number = '+91' + to_number.replace('-', '').replace(' ', '')
            
            logger.info(f"📤 Sending WhatsApp to {to_number} ({business_name or 'Unknown'})")
            
            if self.auto_mode and instant:
                # INSTANT SEND - Khud se bhej dega!
                try:
                    kit.sendwhatmsg_instantly(
                        phone_no=to_number,
                        message=message,
                        wait_time=10,
                        tab_close=True,
                        close_time=3
                    )
                    logger.info(f"✅ WhatsApp sent INSTANTLY to {business_name or to_number}")
                    return True
                except Exception as e:
                    logger.warning(f"⚠️ Instant send failed, trying scheduled: {e}")
                    instant = False
            
            if not instant:
                # SCHEDULED SEND - 2 minute baad bhejega
                now = datetime.now() + timedelta(minutes=2)
                hour = now.hour
                minute = now.minute
                
                kit.sendwhatmsg(
                    phone_no=to_number,
                    message=message,
                    time_hour=hour,
                    time_min=minute,
                    wait_time=15,
                    tab_close=True,
                    close_time=3
                )
                
                logger.info(f"✅ WhatsApp scheduled for {hour}:{minute} to {business_name or to_number}")
                return True
            
        except Exception as e:
            logger.error(f"❌ WhatsApp failed for {to_number}: {str(e)}")
            # Fallback: Open WhatsApp Web manually
            try:
                self._open_whatsapp_web(to_number, message)
                logger.info(f"⚠️ Opened WhatsApp Web for {business_name or to_number}")
                return True
            except:
                return False
    
    def _open_whatsapp_web(self, phone: str, message: str):
        """
        Fallback: Open WhatsApp Web with pre-filled message.
        
        Args:
            phone: Phone number
            message: Message text
        """
        message_encoded = urllib.parse.quote(message)
        url = f"https://web.whatsapp.com/send?phone={phone}&text={message_encoded}"
        webbrowser.open(url)
        time.sleep(2)
    
    def send_bulk_messages(self, recipients: list[dict], 
                          delay_seconds: int = 30) -> dict:
        """
        Send bulk WhatsApp messages AUTOMATICALLY.
        
        Args:
            recipients: List of dicts with 'phone', 'message', 'business_name' keys
            delay_seconds: Seconds between each message (default: 30s)
        
        Returns:
            Dict with 'sent', 'failed', 'total' counts
        """
        results = {'sent': 0, 'failed': 0, 'total': len(recipients)}
        
        logger.info(f"🚀 Starting bulk WhatsApp campaign for {len(recipients)} leads")
        
        for i, recipient in enumerate(recipients):
            phone = recipient.get('phone')
            message = recipient.get('message')
            business_name = recipient.get('business_name', '')
            
            if not phone or not message:
                logger.warning(f"⚠️ Skipping {business_name}: Missing phone or message")
                results['failed'] += 1
                continue
            
            logger.info(f"[{i+1}/{len(recipients)}] Sending to {business_name}...")
            
            # Send message
            success = self.send_message(phone, message, business_name, instant=True)
            
            if success:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            # Delay between messages (anti-spam)
            if i < len(recipients) - 1 and delay_seconds > 0:
                logger.info(f"⏳ Waiting {delay_seconds}s before next message...")
                time.sleep(delay_seconds)
        
        logger.info(f"✅ Bulk WhatsApp complete: {results['sent']}/{results['total']} sent")
        return results


def create_whatsapp_sender(phone_number: str = "8700048490", auto_mode: bool = True) -> WhatsAppSender:
    """
    Create WhatsApp sender instance.
    
    Args:
        phone_number: Your WhatsApp number
        auto_mode: If True, sends automatically
    
    Returns:
        WhatsAppSender instance
    """
    return WhatsAppSender(phone_number, auto_mode)
