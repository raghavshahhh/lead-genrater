"""FREE WhatsApp Auto-Chat Bot using Selenium + Gemini AI."""

import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class WhatsAppBot:
    """FREE WhatsApp automation bot with AI conversations."""
    
    def __init__(self, ai_assistant=None):
        """
        Initialize WhatsApp bot.
        
        Args:
            ai_assistant: GeminiAI instance for generating replies
        """
        self.ai_assistant = ai_assistant
        self.driver = None
        self.conversation_history = {}
        logger.info("WhatsApp Bot initialized")
    
    def start(self):
        """Start WhatsApp Web session."""
        logger.info("Starting WhatsApp Web...")
        
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=./whatsapp_session")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("https://web.whatsapp.com")
        
        logger.info("✅ WhatsApp Web opened")
        logger.info("📱 Scan QR code with your phone...")
        
        # Wait for QR scan
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            logger.info("✅ QR code scanned! WhatsApp ready!")
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"QR scan timeout: {str(e)}")
            return False
    
    def send_message(self, phone_number: str, message: str) -> bool:
        """
        Send WhatsApp message to a phone number.
        
        Args:
            phone_number: Phone with country code (e.g., "919876543210")
            message: Message text to send
        
        Returns:
            True if sent successfully
        """
        try:
            # Format URL
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            self.driver.get(url)
            time.sleep(5)
            
            # Find message box
            message_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # Type message
            message_box.click()
            message_box.send_keys(message)
            time.sleep(1)
            
            # Send
            message_box.send_keys(Keys.ENTER)
            
            logger.info(f"✅ Message sent to {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            return False
    
    def get_last_message(self) -> dict:
        """
        Get the last received message from current chat.
        
        Returns:
            Dict with 'text', 'time', 'is_from_me' keys
        """
        try:
            # Find all message bubbles
            messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-")]')
            
            if not messages:
                return None
            
            # Get last message
            last_msg = messages[-1]
            
            # Check if it's from me or them
            is_from_me = "message-out" in last_msg.get_attribute("class")
            
            # Get message text
            try:
                text_elem = last_msg.find_element(By.XPATH, './/span[@class="selectable-text copyable-text"]')
                text = text_elem.text
            except:
                text = ""
            
            # Get timestamp
            try:
                time_elem = last_msg.find_element(By.XPATH, './/span[@data-testid="msg-time"]')
                msg_time = time_elem.text
            except:
                msg_time = datetime.now().strftime("%H:%M")
            
            return {
                'text': text,
                'time': msg_time,
                'is_from_me': is_from_me
            }
            
        except Exception as e:
            logger.error(f"Error getting last message: {str(e)}")
            return None
    
    def wait_for_reply(self, timeout: int = 300) -> str:
        """
        Wait for client to reply.
        
        Args:
            timeout: Maximum wait time in seconds
        
        Returns:
            Reply text or None
        """
        logger.info("⏳ Waiting for client reply...")
        
        start_time = time.time()
        last_checked_msg = None
        
        while (time.time() - start_time) < timeout:
            msg = self.get_last_message()
            
            if msg and not msg['is_from_me'] and msg['text'] != last_checked_msg:
                logger.info(f"📩 Client replied: {msg['text']}")
                return msg['text']
            
            last_checked_msg = msg['text'] if msg else None
            time.sleep(5)
        
        logger.warning("⏰ Reply timeout")
        return None
    
    def generate_ai_reply(self, client_message: str, business_name: str, 
                         conversation_context: list = None) -> str:
        """
        Generate AI reply using Gemini.
        
        Args:
            client_message: What client said
            business_name: Business name for context
            conversation_context: Previous messages
        
        Returns:
            AI generated reply
        """
        if not self.ai_assistant:
            return "Thanks for your message! I'll get back to you soon."
        
        # Build context
        context = "\n".join(conversation_context) if conversation_context else ""
        
        prompt = f"""You are Raghav from RagsPro.com - a professional digital agency. You're texting on WhatsApp like a REAL person.

Business: {business_name}

Previous messages:
{context}

Client just said: "{client_message}"

CRITICAL RULES - Sound 100% HUMAN:
1. Reply like you're texting a friend (casual, natural)
2. Use Indian texting style (mix of Hindi-English if natural)
3. Show you READ their message (acknowledge what they said)
4. Be helpful, not pushy
5. Use emojis naturally (1-2 max, not forced)
6. Keep it SHORT (30-40 words max)
7. Match their energy (if they're brief, you be brief)
8. NO formal language, NO "Dear", NO business jargon
9. Sound excited but not desperate
10. If they show interest, suggest a quick 10-min call

YOUR AGENCY - RagsPro.com:
- Professional digital agency
- Specializes in websites, SEO, digital marketing
- Helped 100+ businesses get online
- Known for quality work and results

RESPONSE STRATEGIES:
- If they ask price: "Depends on features, but starts from ₹12k. Can show you our portfolio in 10 mins?"
- If they say yes/interested: "Awesome! 😊 Can I call you in 5 mins? Will show you some examples"
- If they're busy: "No worries! When's a good time? Evening works?"
- If they ask questions: Answer directly, mention RagsPro.com expertise
- If they're skeptical: "Totally get it. Check ragspro.com for our work. Happy to show live examples"
- If they ask about agency: "We're RagsPro.com - helped 100+ businesses. Can share client examples"

Write ONLY your reply (natural, human, conversational):"""
        
        try:
            response = self.ai_assistant.model.generate_content(prompt)
            reply = response.text.strip()
            logger.info(f"🤖 AI generated reply: {reply[:50]}...")
            return reply
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            return "Thanks! Can we schedule a quick 10-min call to discuss? 📞"
    
    def auto_conversation(self, phone_number: str, business_name: str, 
                         initial_message: str, max_exchanges: int = 5) -> dict:
        """
        Run automatic conversation with a lead.
        
        Args:
            phone_number: Lead's WhatsApp number
            business_name: Business name
            initial_message: First message to send
            max_exchanges: Maximum back-and-forth exchanges
        
        Returns:
            Dict with conversation log and status
        """
        logger.info(f"🤖 Starting auto-conversation with {business_name}")
        
        conversation = []
        
        # Send initial message
        if self.send_message(phone_number, initial_message):
            conversation.append({
                'from': 'bot',
                'message': initial_message,
                'time': datetime.now().strftime("%H:%M")
            })
        else:
            return {'status': 'failed', 'conversation': conversation}
        
        # Conversation loop
        for exchange in range(max_exchanges):
            logger.info(f"💬 Exchange {exchange + 1}/{max_exchanges}")
            
            # Wait for reply
            reply = self.wait_for_reply(timeout=300)
            
            if not reply:
                logger.info("⏰ No reply received, ending conversation")
                break
            
            conversation.append({
                'from': 'client',
                'message': reply,
                'time': datetime.now().strftime("%H:%M")
            })
            
            # Check if lead is hot
            hot_keywords = ['yes', 'haan', 'interested', 'call', 'demo', 'sure', 'ok']
            if any(keyword in reply.lower() for keyword in hot_keywords):
                logger.info("🔥 HOT LEAD DETECTED!")
                
                # Send confirmation
                final_msg = "Great! I'll call you in 5 minutes. Keep your phone handy! 📞"
                self.send_message(phone_number, final_msg)
                conversation.append({
                    'from': 'bot',
                    'message': final_msg,
                    'time': datetime.now().strftime("%H:%M")
                })
                
                return {
                    'status': 'hot_lead',
                    'conversation': conversation,
                    'action': 'CALL NOW!'
                }
            
            # Generate AI reply
            context = [f"{msg['from']}: {msg['message']}" for msg in conversation[-4:]]
            ai_reply = self.generate_ai_reply(reply, business_name, context)
            
            # Send AI reply
            time.sleep(2)  # Human-like delay
            if self.send_message(phone_number, ai_reply):
                conversation.append({
                    'from': 'bot',
                    'message': ai_reply,
                    'time': datetime.now().strftime("%H:%M")
                })
            
            time.sleep(3)
        
        return {
            'status': 'completed',
            'conversation': conversation,
            'action': 'Follow up later'
        }
    
    def close(self):
        """Close WhatsApp session."""
        if self.driver:
            self.driver.quit()
            logger.info("WhatsApp session closed")


def create_whatsapp_bot(ai_assistant=None) -> WhatsAppBot:
    """
    Create WhatsApp bot instance.
    
    Args:
        ai_assistant: GeminiAI instance
    
    Returns:
        WhatsAppBot instance
    """
    return WhatsAppBot(ai_assistant)
