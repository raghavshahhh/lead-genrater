"""Property-based and unit tests for scraper module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from hypothesis import given, strategies as st, settings

from src.scraper import search_places, search_places_batch


# Feature: lead-generation-bot, Property 2: API requests include correct parameters
@given(query=st.text(min_size=1, max_size=100))
@settings(max_examples=50)
def test_property_api_parameters(query):
    """
    Property 2: API requests include correct parameters.
    
    For any generated query string, when submitted to the scraper,
    the resulting SerpAPI request should include the "google_maps"
    engine parameter and the exact query string.
    
    Validates: Requirements 1.2
    """
    api_key = "test_api_key"
    
    with patch('src.scraper.GoogleSearch') as mock_search:
        # Setup mock
        mock_instance = Mock()
        mock_instance.get_dict.return_value = {"local_results": []}
        mock_search.return_value = mock_instance
        
        # Call function
        search_places(query, api_key)
        
        # Verify GoogleSearch was called with correct parameters
        mock_search.assert_called_once()
        call_args = mock_search.call_args[0][0]
        
        assert call_args["engine"] == "google_maps"
        assert call_args["q"] == query
        assert call_args["type"] == "search"
        assert call_args["api_key"] == api_key


# Feature: lead-generation-bot, Property 3: Scraper extracts local results
@given(
    num_results=st.integers(min_value=0, max_value=50)
)
@settings(max_examples=50)
def test_property_result_extraction(num_results):
    """
    Property 3: Scraper extracts local results.
    
    For any valid SerpAPI response containing a "local_results" field,
    the scraper should extract and return the contents of that field as a list.
    
    Validates: Requirements 1.3
    """
    api_key = "test_api_key"
    query = "test query"
    
    # Generate mock results
    mock_results = [{"title": f"Business {i}"} for i in range(num_results)]
    
    with patch('src.scraper.GoogleSearch') as mock_search:
        # Setup mock
        mock_instance = Mock()
        mock_instance.get_dict.return_value = {"local_results": mock_results}
        mock_search.return_value = mock_instance
        
        # Call function
        results = search_places(query, api_key)
        
        # Verify results match
        assert len(results) == num_results
        assert results == mock_results


# Feature: lead-generation-bot, Property 4: Query failures don't halt processing
@given(
    num_queries=st.integers(min_value=1, max_value=10),
    num_failures=st.integers(min_value=0, max_value=10)
)
@settings(max_examples=50, deadline=None)
def test_property_error_resilience(num_queries, num_failures):
    """
    Property 4: Query failures don't halt processing.
    
    For any list of queries where some queries fail, the system should
    continue processing all remaining queries and return results from
    successful queries.
    
    Validates: Requirements 1.5
    """
    # Ensure failures don't exceed queries
    num_failures = min(num_failures, num_queries)
    
    api_key = "test_api_key"
    queries = [f"query_{i}" for i in range(num_queries)]
    
    # Determine which queries will fail
    failing_indices = set(range(num_failures))
    
    with patch('src.scraper.GoogleSearch') as mock_search, patch('src.scraper.time.sleep'):
        def side_effect(params):
            query_idx = int(params["q"].split("_")[1])
            mock_instance = Mock()
            
            if query_idx in failing_indices:
                # Simulate failure
                mock_instance.get_dict.side_effect = Exception("API Error")
            else:
                # Simulate success
                mock_instance.get_dict.return_value = {
                    "local_results": [{"title": f"Result for {params['q']}"}]
                }
            
            return mock_instance
        
        mock_search.side_effect = side_effect
        
        # Call batch function
        results = search_places_batch(queries, api_key)
        
        # Verify all queries were attempted
        assert len(results) == num_queries
        
        # Verify successful queries have results
        for i, query in enumerate(queries):
            if i not in failing_indices:
                assert len(results[query]) > 0
            else:
                assert len(results[query]) == 0


# Unit tests for edge cases
def test_network_timeout_with_retry():
    """Test that network timeout triggers retry with exponential backoff."""
    api_key = "test_api_key"
    query = "test query"
    
    with patch('src.scraper.GoogleSearch') as mock_search:
        with patch('src.scraper.time.sleep') as mock_sleep:
            # Setup mock to fail twice then succeed
            mock_instance = Mock()
            mock_instance.get_dict.side_effect = [
                Exception("Timeout"),
                Exception("Timeout"),
                {"local_results": [{"title": "Success"}]}
            ]
            mock_search.return_value = mock_instance
            
            # Call function
            results = search_places(query, api_key, max_retries=3)
            
            # Verify retries occurred
            assert mock_instance.get_dict.call_count == 3
            assert mock_sleep.call_count == 2
            
            # Verify exponential backoff
            mock_sleep.assert_any_call(1)  # 2^0
            mock_sleep.assert_any_call(2)  # 2^1
            
            # Verify eventual success
            assert len(results) == 1


def test_max_retries_exceeded():
    """Test that max retries exceeded logs error and returns empty list."""
    api_key = "test_api_key"
    query = "test query"
    
    with patch('src.scraper.GoogleSearch') as mock_search:
        with patch('src.scraper.time.sleep'):
            # Setup mock to always fail
            mock_instance = Mock()
            mock_instance.get_dict.side_effect = Exception("Persistent Error")
            mock_search.return_value = mock_instance
            
            # Call function
            results = search_places(query, api_key, max_retries=3)
            
            # Verify all retries were attempted
            assert mock_instance.get_dict.call_count == 3
            
            # Verify empty list returned
            assert results == []


def test_malformed_response():
    """Test that malformed response (missing local_results) is handled."""
    api_key = "test_api_key"
    query = "test query"
    
    with patch('src.scraper.GoogleSearch') as mock_search:
        # Setup mock with malformed response
        mock_instance = Mock()
        mock_instance.get_dict.return_value = {"error": "No results"}
        mock_search.return_value = mock_instance
        
        # Call function
        results = search_places(query, api_key)
        
        # Verify empty list returned
        assert results == []


def test_empty_local_results():
    """Test that empty local_results returns empty list."""
    api_key = "test_api_key"
    query = "test query"
    
    with patch('src.scraper.GoogleSearch') as mock_search:
        # Setup mock with empty results
        mock_instance = Mock()
        mock_instance.get_dict.return_value = {"local_results": []}
        mock_search.return_value = mock_instance
        
        # Call function
        results = search_places(query, api_key)
        
        # Verify empty list returned
        assert results == []
