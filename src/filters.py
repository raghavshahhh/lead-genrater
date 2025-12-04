"""Filtering and transformation module for Lead Generation Bot."""

from datetime import datetime, timezone
from typing import Optional


def is_good_lead(place: dict) -> bool:
    """
    Determine if a business meets quality criteria.
    
    Criteria:
    - Rating ≥ 4.0
    - Reviews ≥ 20
    - No website present
    
    Args:
        place: Business dictionary from SerpAPI
    
    Returns:
        True if business meets all criteria, False otherwise
    """
    # Check rating
    rating = place.get("rating")
    if rating is None or rating < 4.0:
        return False
    
    # Check reviews
    reviews = place.get("reviews")
    if reviews is None or reviews < 20:
        return False
    
    # Check website (should NOT have a website)
    website = place.get("website")
    if website:  # If website exists and is not empty
        return False
    
    return True


def transform_place(place: dict, query: str) -> dict:
    """
    Transform SerpAPI place data into structured lead record.
    
    Args:
        place: Business dictionary from SerpAPI
        query: Original search query
    
    Returns:
        Lead dictionary with all required fields
    """
    # Extract address components
    address = place.get("address", "")
    address_parts = [p.strip() for p in address.split(",")]
    
    # Try to parse city, state, country from address
    city = ""
    state = None
    country = ""
    
    if len(address_parts) >= 2:
        city = address_parts[0]
        country = address_parts[-1]
        if len(address_parts) >= 3:
            state = address_parts[-2]
    
    # Get GPS coordinates link
    gps_link = place.get("gps_coordinates", {}).get("link", "")
    
    # Create lead record
    lead = {
        "business_name": place.get("title", ""),
        "category": place.get("type", ""),
        "city": city,
        "state": state,
        "country": country,
        "rating": place.get("rating", 0.0),
        "reviews_count": place.get("reviews", 0),
        "phone": place.get("phone"),
        "website_url": place.get("website"),
        "has_website": bool(place.get("website")),
        "maps_url": gps_link,
        "place_id": place.get("place_id", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_query": query,
        "status": "Not Contacted"
    }
    
    return lead
