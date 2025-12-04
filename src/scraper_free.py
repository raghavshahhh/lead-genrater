"""REAL Google Maps scraper using Outscraper API - FREE TIER!"""

import logging
import requests
import time

logger = logging.getLogger(__name__)

# Outscraper FREE API (100 requests/month)
OUTSCRAPER_API_KEY = "your_key_here"  # Get from outscraper.com


def scrape_google_maps_outscraper(query: str, max_results: int = 20) -> list[dict]:
    """
    Scrape REAL Google Maps data using Outscraper API (FREE tier).
    
    FREE TIER: 100 requests/month
    Sign up: https://outscraper.com/
    
    Args:
        query: Search query (e.g., "day care in Gurgaon")
        max_results: Maximum number of results
    
    Returns:
        List of REAL business dictionaries
    """
    results = []
    
    try:
        logger.info(f"🔍 Scraping REAL data for: {query}")
        
        # Outscraper API endpoint
        url = "https://api.app.outscraper.com/maps/search-v3"
        
        params = {
            'query': query,
            'limit': min(max_results, 20),  # Max 20 per request
            'language': 'en',
            'region': 'in'
        }
        
        headers = {
            'X-API-KEY': OUTSCRAPER_API_KEY
        }
        
        # Make API request
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse results
            if data and len(data) > 0:
                for item in data[0]:  # First result set
                    try:
                        business = {
                            'title': item.get('name', ''),
                            'rating': item.get('rating'),
                            'reviews': item.get('reviews', 0),
                            'address': item.get('full_address', ''),
                            'phone': item.get('phone'),
                            'website': item.get('site'),
                            'type': item.get('type', ''),
                            'place_id': item.get('place_id', ''),
                            'gps_coordinates': {
                                'link': f"https://www.google.com/maps/place/?q=place_id:{item.get('place_id', '')}"
                            }
                        }
                        results.append(business)
                        logger.info(f"✅ Found: {business['title']} ({business['rating']}★)")
                    except Exception as e:
                        logger.warning(f"Error parsing business: {e}")
                        continue
                
                logger.info(f"✅ Scraped {len(results)} REAL businesses")
            else:
                logger.warning("No results found")
        
        elif response.status_code == 402:
            logger.error("❌ Outscraper API: Out of credits. Using fallback...")
            return scrape_google_maps_serper(query, max_results)
        
        else:
            logger.error(f"❌ Outscraper API error: {response.status_code}")
            logger.info("Trying fallback method...")
            return scrape_google_maps_serper(query, max_results)
            
    except Exception as e:
        logger.error(f"Error in Outscraper scraping: {str(e)}")
        logger.info("Trying fallback method...")
        return scrape_google_maps_serper(query, max_results)
    
    return results


def scrape_google_maps_serper(query: str, max_results: int = 20) -> list[dict]:
    """
    Scrape REAL Google Maps data using Serper API (FREE tier).
    
    FREE TIER: 2,500 searches/month
    Sign up: https://serper.dev/
    
    Args:
        query: Search query
        max_results: Maximum results
    
    Returns:
        List of REAL business dictionaries
    """
    results = []
    
    try:
        logger.info(f"🔍 Using Serper API for: {query}")
        
        url = "https://google.serper.dev/maps"
        
        payload = {
            'q': query,
            'num': min(max_results, 20)
        }
        
        headers = {
            'X-API-KEY': 'your_serper_key_here',  # Get from serper.dev
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            places = data.get('places', [])
            
            for place in places:
                try:
                    business = {
                        'title': place.get('title', ''),
                        'rating': place.get('rating'),
                        'reviews': place.get('reviews', 0),
                        'address': place.get('address', ''),
                        'phone': place.get('phoneNumber'),
                        'website': place.get('website'),
                        'type': place.get('type', ''),
                        'place_id': place.get('placeId', ''),
                        'gps_coordinates': {
                            'link': place.get('link', '')
                        }
                    }
                    results.append(business)
                    logger.info(f"✅ Found: {business['title']} ({business['rating']}★)")
                except Exception as e:
                    logger.warning(f"Error parsing business: {e}")
                    continue
            
            logger.info(f"✅ Scraped {len(results)} REAL businesses")
        else:
            logger.error(f"❌ Serper API error: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error in Serper scraping: {str(e)}")
    
    return results


def search_places_free(query: str, max_results: int = 20) -> list[dict]:
    """
    Search for REAL businesses on Google Maps.
    
    Uses FREE APIs:
    1. Outscraper (100 requests/month)
    2. Serper (2,500 searches/month) - fallback
    
    Args:
        query: Search string (e.g., "day care in Gurgaon")
        max_results: Maximum results to return
    
    Returns:
        List of REAL business dictionaries
    """
    logger.info("=" * 80)
    logger.info("🚀 REAL DATA SCRAPING (No fake/demo data)")
    logger.info("=" * 80)
    
    # Try Outscraper first (best quality)
    results = scrape_google_maps_outscraper(query, max_results)
    
    # If no results, try Serper
    if not results:
        logger.info("Trying Serper API...")
        results = scrape_google_maps_serper(query, max_results)
    
    # If still no results, log error
    if not results:
        logger.error("❌ No REAL data available. Please add API keys:")
        logger.error("   1. Outscraper: https://outscraper.com/ (100 free/month)")
        logger.error("   2. Serper: https://serper.dev/ (2,500 free/month)")
        logger.error("   3. SerpAPI: https://serpapi.com/ (100 free/month)")
    
    return results
