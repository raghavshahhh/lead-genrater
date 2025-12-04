"""Google Maps scraper using SerpAPI - REAL DATA!"""

import logging
from serpapi import GoogleSearch
import time

logger = logging.getLogger(__name__)


def search_places(query: str, api_key: str) -> list[dict]:
    """
    Search Google Maps via SerpAPI for REAL business data.
    
    Args:
        query: Search string (e.g., "baby care in Delhi, India")
        api_key: SerpAPI key
    
    Returns:
        List of REAL business dictionaries
    """
    results = []
    
    try:
        logger.info(f"🔍 Searching REAL data: {query}")
        
        # SerpAPI parameters
        params = {
            "engine": "google_maps",
            "q": query,
            "type": "search",
            "api_key": api_key
        }
        
        # Make API request
        search = GoogleSearch(params)
        data = search.get_dict()
        
        # Extract local results
        local_results = data.get("local_results", [])
        
        if local_results:
            for place in local_results:
                try:
                    business = {
                        'title': place.get('title', ''),
                        'rating': place.get('rating'),
                        'reviews': place.get('reviews', 0),
                        'address': place.get('address', ''),
                        'phone': place.get('phone'),
                        'website': place.get('website'),
                        'type': place.get('type', ''),
                        'place_id': place.get('place_id', ''),
                        'gps_coordinates': place.get('gps_coordinates', {})
                    }
                    results.append(business)
                    logger.info(f"✅ Found: {business['title']} ({business.get('rating', 'N/A')}★)")
                except Exception as e:
                    logger.warning(f"Error parsing business: {e}")
                    continue
            
            logger.info(f"✅ Scraped {len(results)} REAL businesses from SerpAPI")
        else:
            logger.warning(f"No results found for: {query}")
            
    except Exception as e:
        logger.error(f"SerpAPI error: {str(e)}")
        # Retry once after 2 seconds
        try:
            logger.info("Retrying in 2 seconds...")
            time.sleep(2)
            search = GoogleSearch(params)
            data = search.get_dict()
            local_results = data.get("local_results", [])
            
            for place in local_results:
                try:
                    business = {
                        'title': place.get('title', ''),
                        'rating': place.get('rating'),
                        'reviews': place.get('reviews', 0),
                        'address': place.get('address', ''),
                        'phone': place.get('phone'),
                        'website': place.get('website'),
                        'type': place.get('type', ''),
                        'place_id': place.get('place_id', ''),
                        'gps_coordinates': place.get('gps_coordinates', {})
                    }
                    results.append(business)
                except:
                    continue
                    
            logger.info(f"✅ Retry successful: {len(results)} businesses")
        except Exception as retry_error:
            logger.error(f"Retry failed: {str(retry_error)}")
    
    return results
