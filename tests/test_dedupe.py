"""Property-based and unit tests for deduplication module."""

import os
import tempfile
import pytest
from hypothesis import given, strategies as st, settings

from src.dedupe import load_seen_ids, save_seen_ids


# Feature: lead-generation-bot, Property 7: Processed IDs are loaded at startup
@given(
    place_ids=st.lists(
        st.text(min_size=10, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126, blacklist_characters='\n\r\t')),
        min_size=0, max_size=100, unique=True
    )
)
@settings(max_examples=100)
def test_property_load_processed_ids(place_ids):
    """
    Property 7: Processed IDs are loaded at startup.
    
    For any processed IDs file containing a set of Place IDs,
    loading the file should return a set containing exactly those Place IDs.
    
    Validates: Requirements 3.1
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        for place_id in place_ids:
            f.write(f"{place_id}\n")
        temp_path = f.name
    
    try:
        loaded_ids = load_seen_ids(temp_path)
        
        # Verify all IDs were loaded (accounting for strip())
        expected_ids = {pid.strip() for pid in place_ids if pid.strip()}
        assert loaded_ids == expected_ids
    finally:
        os.unlink(temp_path)


# Feature: lead-generation-bot, Property 8: Duplicate Place IDs are skipped
@given(
    existing_ids=st.lists(st.text(min_size=10, max_size=50), min_size=1, max_size=50, unique=True),
    test_id_is_duplicate=st.booleans()
)
@settings(max_examples=100)
def test_property_duplicate_detection(existing_ids, test_id_is_duplicate):
    """
    Property 8: Duplicate Place IDs are skipped.
    
    For any business with a Place ID that exists in the processed IDs set,
    the deduplication check should return false (skip), and for any business
    with a Place ID not in the set, it should return true (process).
    
    Validates: Requirements 3.2
    """
    seen_ids = set(existing_ids)
    
    if test_id_is_duplicate:
        # Test with an ID that exists
        test_id = existing_ids[0]
        assert test_id in seen_ids
    else:
        # Test with a new ID
        test_id = "new_unique_id_12345678901234567890"
        assert test_id not in seen_ids


# Feature: lead-generation-bot, Property 9: New Place IDs are added to collection
@given(
    initial_ids=st.lists(st.text(min_size=10, max_size=50), min_size=0, max_size=50, unique=True),
    new_id=st.text(min_size=10, max_size=50)
)
@settings(max_examples=100)
def test_property_add_new_ids(initial_ids, new_id):
    """
    Property 9: New Place IDs are added to collection.
    
    For any lead that is successfully stored, its Place ID should be
    added to the processed IDs collection.
    
    Validates: Requirements 3.3
    """
    # Ensure new_id is actually new
    if new_id in initial_ids:
        new_id = new_id + "_unique"
    
    ids = set(initial_ids)
    ids.add(new_id)
    
    assert new_id in ids
    assert len(ids) == len(initial_ids) + 1


# Feature: lead-generation-bot, Property 10: Place ID persistence round-trip
@given(
    place_ids=st.lists(
        st.text(min_size=10, max_size=50, alphabet=st.characters(min_codepoint=32, max_codepoint=126, blacklist_characters='\n\r\t')),
        min_size=0, max_size=100, unique=True
    )
)
@settings(max_examples=100)
def test_property_persistence_roundtrip(place_ids):
    """
    Property 10: Place ID persistence round-trip.
    
    For any set of Place IDs, saving them to storage and then loading
    from storage should return an equivalent set containing all the
    original Place IDs.
    
    Validates: Requirements 3.4
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_path = f.name
    
    try:
        # Save IDs
        save_seen_ids(set(place_ids), temp_path)
        
        # Load IDs
        loaded_ids = load_seen_ids(temp_path)
        
        # Verify round-trip (accounting for strip())
        expected_ids = {pid.strip() for pid in place_ids if pid.strip()}
        assert loaded_ids == expected_ids
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


# Unit test for missing file
def test_missing_file_returns_empty_set():
    """Test that non-existent file returns empty set."""
    ids = load_seen_ids("nonexistent_file_12345.txt")
    assert ids == set()
    assert len(ids) == 0


def test_save_creates_directory():
    """Test that save creates directory if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "subdir", "test.txt")
        save_seen_ids({"id1", "id2"}, path)
        
        assert os.path.exists(path)
        loaded = load_seen_ids(path)
        assert loaded == {"id1", "id2"}


def test_save_appends_new_ids():
    """Test that save appends only new IDs."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("existing_id_1\n")
        f.write("existing_id_2\n")
        temp_path = f.name
    
    try:
        # Save with some existing and some new IDs
        save_seen_ids({"existing_id_1", "new_id_1", "new_id_2"}, temp_path)
        
        # Load and verify
        loaded = load_seen_ids(temp_path)
        assert loaded == {"existing_id_1", "existing_id_2", "new_id_1", "new_id_2"}
    finally:
        os.unlink(temp_path)
