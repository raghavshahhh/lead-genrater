"""FREE email sending using Gmail SMTP (500 emails/day free)."""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger(__name__)


class GmailSender:
    """FREE email sender using Gmail SMTP."""
    
    def __init__(self, gmail_address: str, gmail_app_password: str):
        """
        Initialize Gmail sender.
        
        Args:
            gmail_address: Your Gmail address
            gmail_app_password: Gmail App Password (not regular password)
                Generate at: https://myaccount.google.com/apppasswords
        """
        self.gmail_address = gmail_address
        self.gmail_app_password = gmail_app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        logger.info(f"Gmail sender initialized: {gmail_address}")
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   business_name: Optional[str] = None) -> bool:
        """
        Send email via Gmail SMTP (FREE - 500/day limit).
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (can be HTML or plain text)
            business_name: Optional business name for logging
        
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Add professional signature
            signature = """

Best regards,
Raghav Shah
Founder, Ragspro.com - Software Development Agency

📞 +918700048490
📧 raghav@ragspro.com
🌐 ragspro.com

Connect:
💼 LinkedIn: linkedin.com/in/raghavshahhh
💻 GitHub: github.com/raghavshahhhh
📸 Instagram: instagram.com/raghavshahhhh
🎥 YouTube: youtube.com/@raghavshahhh
🐦 Twitter: x.com/raghavshahhhh
💼 Fiverr: fiverr.com/s/WEpRvR7"""
            
            full_body = body + signature
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"Raghav - RagsPro.com <{self.gmail_address}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(full_body, 'plain'))
            
            # Connect to Gmail SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_address, self.gmail_app_password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email} ({business_name or 'Unknown'})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_bulk_emails(self, recipients: list[dict], subject_template: str, 
                        body_template: str, delay_seconds: int = 2) -> dict:
        """
        Send bulk emails with rate limiting (FREE Gmail limit: 500/day).
        
        Args:
            recipients: List of dicts with 'email', 'name', 'body' keys
            subject_template: Subject line template
            body_template: Email body template (use {name}, {business_name} placeholders)
            delay_seconds: Delay between emails to avoid spam detection
        
        Returns:
            Dict with 'sent', 'failed', 'total' counts
        """
        import time
        
        results = {'sent': 0, 'failed': 0, 'total': len(recipients)}
        
        for recipient in recipients:
            email = recipient.get('email')
            name = recipient.get('name', 'there')
            business_name = recipient.get('business_name', '')
            custom_body = recipient.get('body', body_template)
            
            if not email:
                logger.warning(f"Skipping recipient with no email: {business_name}")
                results['failed'] += 1
                continue
            
            # Personalize subject and body
            subject = subject_template.format(name=name, business_name=business_name)
            body = custom_body.format(name=name, business_name=business_name)
            
            # Send email
            success = self.send_email(email, subject, body, business_name)
            
            if success:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            # Rate limiting delay
            if delay_seconds > 0:
                time.sleep(delay_seconds)
        
        logger.info(f"Bulk email complete: {results['sent']}/{results['total']} sent")
        return results


def create_gmail_sender(gmail_address: str, gmail_app_password: str) -> GmailSender:
    """
    Create Gmail sender instance.
    
    Args:
        gmail_address: Your Gmail address
        gmail_app_password: Gmail App Password
    
    Returns:
        GmailSender instance
    """
    return GmailSender(gmail_address, gmail_app_password)
