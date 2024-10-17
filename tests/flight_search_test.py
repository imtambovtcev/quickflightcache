import pytest
import json
from unittest.mock import patch
from datetime import datetime, timedelta
# Ensure this matches your file name and import path
from quick_flight_cache import FlightSearch
import os

# Sample API key and host for initializing FlightSearch
API_KEY = "test_api_key"
API_HOST = "test_api_host"


@pytest.fixture
def flight_search():
    # Create a new instance with a temporary cache file
    return FlightSearch(api_key=API_KEY, api_host=API_HOST, cache_file="temp_cache.json")


def test_cache_storage_and_retrieval(flight_search):
    # Sample parameters for testing
    params = {
        "fromEntityId": "KEF",
        "toEntityId": "AYT",
        "departDate": "2024-11-26"
    }
    # Sample response data
    sample_response = {"data": "sample flight data"}

    # Store in cache
    flight_search.store_in_cache(params, sample_response)
    cached_data = flight_search.check_cache(params)

    # Assert that cache retrieval works
    assert cached_data == sample_response


def test_search_flights_cache_hit(flight_search):
    # Sample parameters for testing
    params = {
        "fromEntityId": "KEF",
        "toEntityId": "AYT",
        "departDate": "2024-11-26"
    }
    # Sample response data
    sample_response = {"data": "sample flight data"}

    # Store sample response in cache
    flight_search.store_in_cache(params, sample_response)

    # Run search with update_cache=False and check that it uses cache
    result = flight_search.search_flights(
        "KEF", "AYT", "2024-11-26", update_cache=False)

    # Assert that the result comes from the cache
    assert result == sample_response


@patch("requests.post")
def test_search_flights_api_call(mock_post, flight_search):
    # Mock the API response
    mock_response_data = {"data": "mocked API response"}
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_response_data

    # Ensure the cache is empty to force an API call
    flight_search.cache = {}

    # Perform the search, simulating an API call
    result = flight_search.search_flights(
        "KEF", "AYT", "2024-11-26", update_cache=True)

    # Assert the result matches the mocked API response
    assert result == mock_response_data
    # Verify that the mocked post was called once
    mock_post.assert_called_once()


def teardown_module(module):
    # Remove the temporary cache file after tests
    try:
        os.remove("temp_cache.json")
    except FileNotFoundError:
        pass
