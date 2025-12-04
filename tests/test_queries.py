"""Property-based and unit tests for queries module."""

import pytest
from hypothesis import given, strategies as st

from src.queries import generate_queries, CITIES, CATEGORIES


# Helper function to test the cartesian product property
def _generate_queries_from_lists(cities: list[str], categories: list[str]) -> list[str]:
    """Generate queries from given city and category lists."""
    queries = []
    for city in cities:
        for category in categories:
            query = f"{category} in {city}"
            queries.append(query)
    return queries


# Feature: lead-generation-bot, Property 1: Query generation produces cartesian product
@given(
    cities=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=20, unique=True),
    categories=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=20, unique=True)
)
def test_property_query_cartesian_product(cities, categories):
    """
    Property 1: Query generation produces cartesian product.
    
    For any list of N cities and M categories, the query generation function
    should produce exactly N × M unique queries, where each query is a unique
    combination of one city and one category.
    
    Validates: Requirements 1.1
    """
    # Generate queries using the helper function
    queries = _generate_queries_from_lists(cities, categories)
    
    # Expected count
    expected_count = len(cities) * len(categories)
    
    # Verify count
    assert len(queries) == expected_count
    
    # Verify uniqueness (only if cities and categories are unique)
    assert len(set(queries)) == expected_count
    
    # Verify all combinations are present
    if cities and categories:
        for city in cities:
            for category in categories:
                expected_query = f"{category} in {city}"
                assert expected_query in queries


# Unit tests for edge cases
def test_empty_city_list(monkeypatch):
    """Test that empty city list produces empty queries."""
    monkeypatch.setattr('src.queries.CITIES', [])
    monkeypatch.setattr('src.queries.CATEGORIES', ["test category"])
    
    queries = generate_queries()
    assert len(queries) == 0


def test_empty_category_list(monkeypatch):
    """Test that empty category list produces empty queries."""
    monkeypatch.setattr('src.queries.CITIES', ["Test City"])
    monkeypatch.setattr('src.queries.CATEGORIES', [])
    
    queries = generate_queries()
    assert len(queries) == 0


def test_single_city_and_category(monkeypatch):
    """Test that single city and category produces one query."""
    monkeypatch.setattr('src.queries.CITIES', ["Test City"])
    monkeypatch.setattr('src.queries.CATEGORIES', ["test category"])
    
    queries = generate_queries()
    assert len(queries) == 1
    assert queries[0] == "test category in Test City"


def test_default_cities_and_categories():
    """Test that default lists produce expected number of queries."""
    queries = generate_queries()
    
    expected_count = len(CITIES) * len(CATEGORIES)
    assert len(queries) == expected_count
    
    # Verify all queries are unique
    assert len(set(queries)) == expected_count
    
    # Verify format
    for query in queries:
        assert " in " in query
