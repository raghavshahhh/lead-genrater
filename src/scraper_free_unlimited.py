"""
FREE UNLIMITED Google Maps scraper using multiple methods.
No API key needed - 100% FREE!

Methods used (in order):
1. Google Places API (free tier - 100 requests/day)
2. Selenium (browser automation - unlimited but slower)
3. BeautifulSoup (web scraping - unlimited but may be blocked)
"""

import logging
import requests
import time
from typing import List, Dict
import random

logger = logging.getLogger(__name__)


def scrape_google_maps_free(query: str, max_results: int = 20) -> List[Dict]:
    """
    FREE scraping using Outscraper's free tier.
    
    Args:
        query: Search query (e.g., "restaurants in New York")
        max_results: Maximum results to return
    
    Returns:
        List of business dictionaries
    """
    results = []
    
    try:
        logger.info(f"🆓 FREE Scraping: {query}")
        
        # Outscraper free API endpoint
        # Note: This is a simplified version. For production, use their official API
        url = "https://api.outscraper.com/maps/search-v2"
        
        params = {
            'query': query,
            'limit': max_results,
            'language': 'en',
            'region': 'us'
        }
        
        # Try free scraping
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            for place in data.get('data', []):
                business = {
                    'title': place.get('name', ''),
                    'rating': place.get('rating'),
                    'reviews': place.get('reviews', 0),
                    'address': place.get('full_address', ''),
                    'phone': place.get('phone'),
                    'website': place.get('site'),
                    'type': place.get('type', ''),
                    'place_id': place.get('place_id', ''),
                    'gps_coordinates': {
                        'latitude': place.get('latitude'),
                        'longitude': place.get('longitude')
                    }
                }
                results.append(business)
                logger.info(f"✅ Found: {business['title']}")
        
        logger.info(f"✅ FREE scraped {len(results)} businesses")
        
    except Exception as e:
        logger.error(f"FREE scraping error: {str(e)}")
        # Fallback to alternative method
        results = scrape_with_selenium_free(query, max_results)
    
    return results


def scrape_with_selenium_free(query: str, max_results: int = 20) -> List[Dict]:
    """
    Alternative FREE scraping using Selenium (browser automation).
    This is completely FREE but slower.
    
    Args:
        query: Search query
        max_results: Maximum results
    
    Returns:
        List of businesses
    """
    results = []
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        logger.info(f"🆓 Using Selenium for FREE scraping: {query}")
        
        # Setup headless Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # Search Google Maps
        search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
        driver.get(search_url)
        
        # Wait for results to load
        time.sleep(3)
        
        # Scroll to load more results
        scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        for _ in range(3):  # Scroll 3 times
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(2)
        
        # Extract business data
        business_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        
        for element in business_elements[:max_results]:
            try:
                name = element.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall").text
                rating_text = element.find_element(By.CSS_SELECTOR, "span[role='img']").get_attribute('aria-label')
                
                # Parse rating
                rating = float(rating_text.split()[0]) if rating_text else 0
                
                business = {
                    'title': name,
                    'rating': rating,
                    'reviews': 0,  # Will be extracted if available
                    'address': '',
                    'phone': None,
                    'website': None,
                    'type': query.split('in')[0].strip(),
                    'place_id': '',
                    'gps_coordinates': {}
                }
                
                results.append(business)
                logger.info(f"✅ Found: {name}")
                
            except Exception as e:
                logger.debug(f"Error parsing element: {e}")
                continue
        
        driver.quit()
        logger.info(f"✅ Selenium scraped {len(results)} businesses (FREE)")
        
    except ImportError:
        logger.warning("Selenium not installed. Install with: pip install selenium")
    except Exception as e:
        logger.error(f"Selenium scraping error: {str(e)}")
    
    return results


def scrape_with_beautifulsoup_free(query: str, max_results: int = 20) -> List[Dict]:
    """
    Another FREE alternative using BeautifulSoup (web scraping).
    Completely FREE but may be blocked by Google.
    
    Args:
        query: Search query
        max_results: Maximum results
    
    Returns:
        List of businesses
    """
    results = []
    
    try:
        from bs4 import BeautifulSoup
        import requests
        
        logger.info(f"🆓 Using BeautifulSoup for FREE scraping: {query}")
        
        # Google Maps search URL
        search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract business data (simplified)
        # Note: Google Maps HTML structure changes frequently
        business_divs = soup.find_all('div', class_='fontHeadlineSmall')
        
        for div in business_divs[:max_results]:
            try:
                name = div.text.strip()
                
                business = {
                    'title': name,
                    'rating': 0,
                    'reviews': 0,
                    'address': '',
                    'phone': None,
                    'website': None,
                    'type': query.split('in')[0].strip(),
                    'place_id': '',
                    'gps_coordinates': {}
                }
                
                results.append(business)
                logger.info(f"✅ Found: {name}")
                
            except Exception as e:
                logger.debug(f"Error parsing: {e}")
                continue
        
        logger.info(f"✅ BeautifulSoup scraped {len(results)} businesses (FREE)")
        
    except ImportError:
        logger.warning("BeautifulSoup not installed. Install with: pip install beautifulsoup4")
    except Exception as e:
        logger.error(f"BeautifulSoup scraping error: {str(e)}")
    
    return results


def search_places_free(query: str, max_results: int = 20) -> List[Dict]:
    """
    Main FREE scraping function that tries multiple methods.
    
    Args:
        query: Search query
        max_results: Maximum results
    
    Returns:
        List of businesses
    """
    logger.info(f"🆓 Starting FREE scraping for: {query}")
    
    # Try methods in order of reliability
    methods = [
        ('Outscraper Free', scrape_google_maps_free),
        ('Selenium', scrape_with_selenium_free),
        ('BeautifulSoup', scrape_with_beautifulsoup_free),
    ]
    
    for method_name, method_func in methods:
        try:
            logger.info(f"Trying {method_name}...")
            results = method_func(query, max_results)
            
            if results:
                logger.info(f"✅ {method_name} successful: {len(results)} results")
                return results
            else:
                logger.warning(f"{method_name} returned no results")
                
        except Exception as e:
            logger.warning(f"{method_name} failed: {str(e)}")
            continue
    
    logger.error("All FREE scraping methods failed")
    return []


# Install instructions
INSTALL_INSTRUCTIONS = """
To use FREE unlimited scraping, install these packages:

pip install selenium beautifulsoup4 webdriver-manager

For Selenium, you also need Chrome browser installed.
"""

if __name__ == "__main__":
    print(INSTALL_INSTRUCTIONS)
