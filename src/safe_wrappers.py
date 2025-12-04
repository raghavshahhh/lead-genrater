"""
Safe wrapper functions with error handling for critical operations.
Prevents system crashes and provides graceful fallbacks.
"""

import logging
from functools import wraps
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


def safe_execute(fallback_value: Any = None, log_error: bool = True):
    """
    Decorator to safely execute functions with error handling.
    
    Args:
        fallback_value: Value to return if function fails
        log_error: Whether to log the error
    
    Returns:
        Decorated function that won't crash on errors
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(
                        f"Error in {func.__name__}: {str(e)}",
                        exc_info=True
                    )
                return fallback_value
        return wrapper
    return decorator


def safe_generate_leads(search_function, query: str, api_key: str) -> list:
    """
    Safely generate leads with error handling.
    
    Args:
        search_function: The scraping function to use
        query: Search query
        api_key: API key for scraping
    
    Returns:
        List of leads (empty list if error)
    """
    try:
        logger.info(f"Generating leads for: {query}")
        results = search_function(query, api_key)
        logger.info(f"Successfully generated {len(results)} leads")
        return results
    except Exception as e:
        logger.error(f"Lead generation failed for '{query}': {str(e)}")
        return []  # Return empty list instead of crashing


def safe_send_email(email_sender, to_email: str, subject: str, body: str, business_name: str = None) -> bool:
    """
    Safely send email with error handling.
    
    Args:
        email_sender: Email sender instance
        to_email: Recipient email
        subject: Email subject
        body: Email body
        business_name: Business name for logging
    
    Returns:
        True if sent successfully, False otherwise
    """
    try:
        logger.info(f"Sending email to {business_name or to_email}")
        success = email_sender.send_email(to_email, subject, body, business_name)
        if success:
            logger.info(f"Email sent successfully to {business_name or to_email}")
        else:
            logger.warning(f"Email sending returned False for {business_name or to_email}")
        return success
    except Exception as e:
        logger.error(f"Email failed for {business_name or to_email}: {str(e)}")
        return False


def safe_send_whatsapp(whatsapp_sender, to_number: str, message: str, business_name: str = None) -> bool:
    """
    Safely send WhatsApp message with error handling.
    
    Args:
        whatsapp_sender: WhatsApp sender instance
        to_number: Recipient phone number
        message: Message text
        business_name: Business name for logging
    
    Returns:
        True if sent successfully, False otherwise
    """
    try:
        logger.info(f"Sending WhatsApp to {business_name or to_number}")
        success = whatsapp_sender.send_message(to_number, message, business_name)
        if success:
            logger.info(f"WhatsApp sent successfully to {business_name or to_number}")
        else:
            logger.warning(f"WhatsApp sending returned False for {business_name or to_number}")
        return success
    except Exception as e:
        logger.error(f"WhatsApp failed for {business_name or to_number}: {str(e)}")
        return False


def safe_ai_generate(ai_instance, method_name: str, *args, **kwargs) -> Optional[str]:
    """
    Safely generate AI content with error handling and fallback.
    
    Args:
        ai_instance: AI instance (GeminiAI)
        method_name: Method to call (e.g., 'generate_cold_email')
        *args, **kwargs: Arguments to pass to the method
    
    Returns:
        Generated content or fallback content if error
    """
    try:
        method = getattr(ai_instance, method_name)
        content = method(*args, **kwargs)
        logger.info(f"AI content generated successfully using {method_name}")
        return content
    except Exception as e:
        logger.error(f"AI generation failed for {method_name}: {str(e)}")
        
        # Return fallback content
        if method_name == 'generate_cold_email':
            business_name = args[0] if args else "your business"
            return f"""Hi,

I noticed {business_name} and wanted to reach out.

At Ragspro.com, we help companies like yours ship MVPs in 2-4 weeks using modern tech (React, Node.js, Python).

Recent projects: LawAI, Glow, HimShakti - check ragspro.com

15-min call to explore fit?

Best,
Raghav Shah
Founder, Ragspro.com
+918700048490 | raghav@ragspro.com"""
        
        elif method_name == 'generate_whatsapp_message':
            business_name = args[0] if args else "there"
            return f"""Hey {business_name}! 👋

Raghav from Ragspro.com - we build MVPs in 2-4 weeks.

Built LawAI, Glow, HimShakti - 200+ projects delivered! 💻

15-min call? Reply YES or call +918700048490 📱"""
        
        else:
            return "Content generation failed. Please try again."


def safe_save_leads(save_function, leads: list, *args, **kwargs) -> bool:
    """
    Safely save leads with error handling.
    
    Args:
        save_function: Function to save leads
        leads: List of leads to save
        *args, **kwargs: Additional arguments
    
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        if not leads:
            logger.info("No leads to save")
            return True
        
        logger.info(f"Saving {len(leads)} leads")
        save_function(leads, *args, **kwargs)
        logger.info(f"Successfully saved {len(leads)} leads")
        return True
    except Exception as e:
        logger.error(f"Failed to save leads: {str(e)}")
        return False


def safe_filter_leads(filter_function, leads: list, *args, **kwargs) -> list:
    """
    Safely filter leads with error handling.
    
    Args:
        filter_function: Function to filter leads
        leads: List of leads to filter
        *args, **kwargs: Additional arguments
    
    Returns:
        Filtered leads (original list if error)
    """
    try:
        if not leads:
            logger.info("No leads to filter")
            return []
        
        logger.info(f"Filtering {len(leads)} leads")
        filtered = filter_function(leads, *args, **kwargs)
        logger.info(f"Filtered to {len(filtered)} leads")
        return filtered
    except Exception as e:
        logger.error(f"Lead filtering failed: {str(e)}")
        return leads  # Return original list if filtering fails


# Retry decorator for network operations
def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on failure.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        # Last attempt failed, raise the error
                        logger.error(f"{func.__name__} failed after {max_retries} attempts: {str(e)}")
                        raise
                    else:
                        # Retry after delay
                        logger.warning(f"{func.__name__} attempt {attempt + 1} failed: {str(e)}. Retrying in {delay}s...")
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
            
        return wrapper
    return decorator


# Example usage:
if __name__ == "__main__":
    # Test safe_execute decorator
    @safe_execute(fallback_value="Fallback content", log_error=True)
    def risky_function():
        raise Exception("This will fail")
    
    result = risky_function()
    print(f"Result: {result}")  # Will print "Fallback content"
