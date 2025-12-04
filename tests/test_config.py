"""Property-based and unit tests for configuration module."""

import json
import os
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, strategies as st

from src.config import load_config, ConfigurationError


# Feature: lead-generation-bot, Property 19: Configuration loads all required fields
@given(
    serpapi_key=st.text(min_size=20, max_size=100),
    sheet_id=st.text(min_size=40, max_size=100),
    service_account=st.text(min_size=10, max_size=100),
    min_rating=st.floats(min_value=0.0, max_value=5.0),
    min_reviews=st.integers(min_value=0, max_value=1000),
    max_leads=st.integers(min_value=1, max_value=1000)
)
def test_property_config_loads_all_fields(
    serpapi_key, sheet_id, service_account, min_rating, min_reviews, max_leads
):
    """
    Property 19: Configuration loads all required fields.
    
    For any valid configuration file containing all required fields,
    the configuration loader should successfully load and return all field values.
    
    Validates: Requirements 8.1
    """
    # Create temporary config file
    config_data = {
        "SERPAPI_KEY": serpapi_key,
        "GOOGLE_SHEET_ID": sheet_id,
        "GOOGLE_SERVICE_ACCOUNT_JSON": service_account,
        "MIN_RATING": min_rating,
        "MIN_REVIEWS": min_reviews,
        "MAX_LEADS_PER_RUN": max_leads
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name
    
    try:
        # Load configuration
        loaded_config = load_config(temp_path)
        
        # Verify all fields are present and match
        assert loaded_config["SERPAPI_KEY"] == serpapi_key
        assert loaded_config["GOOGLE_SHEET_ID"] == sheet_id
        assert loaded_config["GOOGLE_SERVICE_ACCOUNT_JSON"] == service_account
        assert loaded_config["MIN_RATING"] == min_rating
        assert loaded_config["MIN_REVIEWS"] == min_reviews
        assert loaded_config["MAX_LEADS_PER_RUN"] == max_leads
    finally:
        os.unlink(temp_path)


# Feature: lead-generation-bot, Property 20: Invalid configuration produces descriptive errors
@given(
    missing_field=st.sampled_from([
        "SERPAPI_KEY", "GOOGLE_SHEET_ID", "GOOGLE_SERVICE_ACCOUNT_JSON",
        "MIN_RATING", "MIN_REVIEWS", "MAX_LEADS_PER_RUN"
    ])
)
def test_property_invalid_config_descriptive_errors(missing_field):
    """
    Property 20: Invalid configuration produces descriptive errors.
    
    For any configuration file with missing or invalid required fields,
    the configuration loader should raise an exception with a descriptive
    error message indicating which field is problematic.
    
    Validates: Requirements 8.4
    """
    # Create config with one missing field
    config_data = {
        "SERPAPI_KEY": "test_key_12345678901234567890",
        "GOOGLE_SHEET_ID": "test_sheet_id_1234567890123456789012345678901234567890",
        "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
        "MIN_RATING": 4.0,
        "MIN_REVIEWS": 20,
        "MAX_LEADS_PER_RUN": 50
    }
    
    # Remove the field
    del config_data[missing_field]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name
    
    try:
        # Should raise ConfigurationError
        with pytest.raises(ConfigurationError) as exc_info:
            load_config(temp_path)
        
        # Error message should mention the missing field
        assert missing_field in str(exc_info.value)
    finally:
        os.unlink(temp_path)


# Unit tests for edge cases
def test_missing_config_file():
    """Test that missing configuration file raises appropriate error."""
    with pytest.raises(ConfigurationError) as exc_info:
        load_config("nonexistent_config.json")
    
    assert "not found" in str(exc_info.value).lower()


def test_invalid_json_syntax():
    """Test that invalid JSON syntax raises appropriate error."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{invalid json content")
        temp_path = f.name
    
    try:
        with pytest.raises(ConfigurationError) as exc_info:
            load_config(temp_path)
        
        assert "json" in str(exc_info.value).lower()
    finally:
        os.unlink(temp_path)


def test_environment_variable_override():
    """Test that environment variables can override config file values."""
    config_data = {
        "SERPAPI_KEY": "file_key",
        "GOOGLE_SHEET_ID": "file_sheet_id_1234567890123456789012345678901234567890",
        "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
        "MIN_RATING": 4.0,
        "MIN_REVIEWS": 20,
        "MAX_LEADS_PER_RUN": 50
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name
    
    try:
        # Set environment variable
        os.environ["SERPAPI_KEY"] = "env_key"
        
        loaded_config = load_config(temp_path)
        
        # Should use environment variable value
        assert loaded_config["SERPAPI_KEY"] == "env_key"
    finally:
        os.unlink(temp_path)
        if "SERPAPI_KEY" in os.environ:
            del os.environ["SERPAPI_KEY"]


def test_invalid_rating_range():
    """Test that MIN_RATING outside valid range raises error."""
    config_data = {
        "SERPAPI_KEY": "test_key_12345678901234567890",
        "GOOGLE_SHEET_ID": "test_sheet_id_1234567890123456789012345678901234567890",
        "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
        "MIN_RATING": 6.0,  # Invalid: > 5.0
        "MIN_REVIEWS": 20,
        "MAX_LEADS_PER_RUN": 50
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name
    
    try:
        with pytest.raises(ConfigurationError) as exc_info:
            load_config(temp_path)
        
        assert "MIN_RATING" in str(exc_info.value)
    finally:
        os.unlink(temp_path)


def test_negative_reviews():
    """Test that negative MIN_REVIEWS raises error."""
    config_data = {
        "SERPAPI_KEY": "test_key_12345678901234567890",
        "GOOGLE_SHEET_ID": "test_sheet_id_1234567890123456789012345678901234567890",
        "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
        "MIN_RATING": 4.0,
        "MIN_REVIEWS": -5,  # Invalid: negative
        "MAX_LEADS_PER_RUN": 50
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name
    
    try:
        with pytest.raises(ConfigurationError) as exc_info:
            load_config(temp_path)
        
        assert "MIN_REVIEWS" in str(exc_info.value)
    finally:
        os.unlink(temp_path)


def test_zero_max_leads():
    """Test that MAX_LEADS_PER_RUN < 1 raises error."""
    config_data = {
        "SERPAPI_KEY": "test_key_12345678901234567890",
        "GOOGLE_SHEET_ID": "test_sheet_id_1234567890123456789012345678901234567890",
        "GOOGLE_SERVICE_ACCOUNT_JSON": "config/service_account.json",
        "MIN_RATING": 4.0,
        "MIN_REVIEWS": 20,
        "MAX_LEADS_PER_RUN": 0  # Invalid: must be at least 1
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_path = f.name
    
    try:
        with pytest.raises(ConfigurationError) as exc_info:
            load_config(temp_path)
        
        assert "MAX_LEADS_PER_RUN" in str(exc_info.value)
    finally:
        os.unlink(temp_path)
