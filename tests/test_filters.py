"""Property-based and unit tests for filters module."""

import pytest
from hypothesis import given, strategies as st, settings
from datetime import datetime

from src.filters import is_good_lead, transform_place


# Feature: lead-generation-bot, Property 5: Filter rejects unqualified businesses
@given(
    rating=st.one_of(st.none(), st.floats(min_value=0.0, max_value=5.0)),
    reviews=st.one_of(st.none(), st.integers(min_value=0, max_value=10000)),
    has_website=st.booleans()
)
@settings(max_examples=100)
def test_property_filter_logic(rating, reviews, has_website):
    """
    Property 5: Filter rejects unqualified businesses.
    
    For any business record, the filter should reject it if any of these
    conditions are true: rating < 4.0, reviews < 20, or website URL is present.
    The filter should accept it only if all conditions are met: rating ≥ 4.0,
    reviews ≥ 20, and no website.
    
    Validates: Requirements 2.1, 2.2, 2.3
    """
    place = {
        "rating": rating,
        "reviews": reviews,
        "website": "https://example.com" if has_website else None
    }
    
    result = is_good_lead(place)
    
    # Determine expected result
    should_pass = (
        rating is not None and rating >= 4.0 and
        reviews is not None and reviews >= 20 and
        not has_website
    )
    
    assert result == should_pass


# Feature: lead-generation-bot, Property 6: Transformation produces complete lead records
@given(
    title=st.text(min_size=1, max_size=100),
    place_type=st.text(min_size=1, max_size=50),
    rating=st.floats(min_value=0.0, max_value=5.0),
    reviews=st.integers(min_value=0, max_value=10000),
    query=st.text(min_size=1, max_size=100)
)
@settings(max_examples=100)
def test_property_transformation_completeness(title, place_type, rating, reviews, query):
    """
    Property 6: Transformation produces complete lead records.
    
    For any business that passes filtering, the transformation function should
    produce a lead record containing all required fields with appropriate types.
    
    Validates: Requirements 2.4
    """
    place = {
        "title": title,
        "type": place_type,
        "rating": rating,
        "reviews": reviews,
        "address": "123 Main St, City, State, Country",
        "phone": "+1234567890",
        "website": None,
        "place_id": "test_place_id_123",
        "gps_coordinates": {"link": "https://maps.google.com/test"}
    }
    
    lead = transform_place(place, query)
    
    # Verify all required fields are present
    required_fields = [
        "business_name", "category", "city", "state", "country",
        "rating", "reviews_count", "phone", "website_url", "has_website",
        "maps_url", "place_id", "created_at", "source_query", "status"
    ]
    
    for field in required_fields:
        assert field in lead, f"Missing required field: {field}"
    
    # Verify types
    assert isinstance(lead["business_name"], str)
    assert isinstance(lead["category"], str)
    assert isinstance(lead["rating"], (int, float))
    assert isinstance(lead["reviews_count"], int)
    assert isinstance(lead["has_website"], bool)
    assert isinstance(lead["status"], str)
    
    # Verify status is set correctly
    assert lead["status"] == "Not Contacted"
    
    # Verify source query is preserved
    assert lead["source_query"] == query


# Unit tests for edge cases
def test_exactly_4_rating_passes():
    """Test that business with exactly 4.0 rating passes."""
    place = {
        "rating": 4.0,
        "reviews": 20,
        "website": None
    }
    assert is_good_lead(place) is True


def test_exactly_20_reviews_passes():
    """Test that business with exactly 20 reviews passes."""
    place = {
        "rating": 4.0,
        "reviews": 20,
        "website": None
    }
    assert is_good_lead(place) is True


def test_null_website_passes():
    """Test that business with null website passes."""
    place = {
        "rating": 4.5,
        "reviews": 50,
        "website": None
    }
    assert is_good_lead(place) is True


def test_empty_string_website_passes():
    """Test that business with empty string website passes."""
    place = {
        "rating": 4.5,
        "reviews": 50,
        "website": ""
    }
    assert is_good_lead(place) is True


def test_below_4_rating_fails():
    """Test that business with rating below 4.0 fails."""
    place = {
        "rating": 3.9,
        "reviews": 50,
        "website": None
    }
    assert is_good_lead(place) is False


def test_below_20_reviews_fails():
    """Test that business with reviews below 20 fails."""
    place = {
        "rating": 4.5,
        "reviews": 19,
        "website": None
    }
    assert is_good_lead(place) is False


def test_with_website_fails():
    """Test that business with website fails."""
    place = {
        "rating": 4.5,
        "reviews": 50,
        "website": "https://example.com"
    }
    assert is_good_lead(place) is False
