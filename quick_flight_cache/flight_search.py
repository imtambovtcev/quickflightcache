import hashlib
import json
import os
import requests
from datetime import datetime, timedelta


class FlightSearch:
    """
    A class to search for flights with caching to minimize API calls. Caches API responses locally
    and retrieves from the cache if the same request is repeated within a specified expiry period.

    Attributes:
        api_key (str): The API key for authentication.
        api_host (str): The host URL for the API.
        cache_file (str): The file path for storing the cache.
        cache_expiry (timedelta): The expiration duration for cache entries.
        cache (dict): A dictionary storing cached responses.
    """

    def __init__(self, api_key, api_host, cache_file="flight_cache.json", cache_expiry_days=1):
        """
        Initializes the FlightSearch instance with API credentials, cache file path, and expiry settings.

        Parameters:
            api_key (str): The API key for accessing the flight search API.
            api_host (str): The host URL for the API.
            cache_file (str): The file path where the cache data is stored. Defaults to "flight_cache.json".
            cache_expiry_days (int): The number of days before cache entries expire. Defaults to 1 day.
        """
        self.api_key = api_key
        self.api_host = api_host
        self.cache_file = cache_file
        self.cache_expiry = timedelta(days=cache_expiry_days)
        self.cache = self.load_cache()

    def load_cache(self):
        """
        Loads the cache from the cache file, if it exists.

        Returns:
            dict: A dictionary containing cached data from the file, or an empty dictionary if the file does not exist.
        """
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        """
        Saves the current cache data to the cache file.
        """
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f)

    def get_cache_key(self, params):
        """
        Generates a unique cache key based on the request parameters.

        Parameters:
            params (dict): The parameters used for the API request.

        Returns:
            str: A unique hash key based on the sorted request parameters.
        """
        key_string = json.dumps(params, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()

    def check_cache(self, params):
        """
        Checks if the response for a given request is available in the cache and is not expired.

        Parameters:
            params (dict): The request parameters.

        Returns:
            dict or None: The cached response data if available and valid, otherwise None.
        """
        key = self.get_cache_key(params)
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - datetime.fromisoformat(entry["timestamp"]) < self.cache_expiry:
                return entry["response"]
        return None

    def store_in_cache(self, params, response):
        """
        Stores a response in the cache with a timestamp.

        Parameters:
            params (dict): The request parameters used for generating the cache key.
            response (dict): The response data from the API to be cached.
        """
        key = self.get_cache_key(params)
        self.cache[key] = {
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        self.save_cache()

    def search_flights(self, fromEntityId, toEntityId, departDate, update_cache=False, **kwargs):
        """
        Searches for flights based on specified parameters, using the cache if possible.

        Parameters:
            fromEntityId (str): The origin entity ID (e.g., airport code).
            toEntityId (str): The destination entity ID (e.g., airport code).
            departDate (str): The departure date in 'YYYY-MM-DD' format.
            update_cache (bool): If True, forces an API call even if data is available in the cache. Defaults to False.
            **kwargs: Additional parameters for the API request, if needed.

        Returns:
            dict: The API response data, either from the cache or from a new API request.
        """
        params = {
            "fromEntityId": fromEntityId,
            "toEntityId": toEntityId,
            "departDate": departDate,
            **kwargs
        }

        if not update_cache:
            cached_response = self.check_cache(params)
            if cached_response:
                print("Using cached data.")
                return cached_response
            else:
                print("Cache miss. Making API request.")

        # Make the API request if cache is not used or needs updating
        url = f"https://{self.api_host}/flights/search-multi-city"
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.api_host,
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers,
                                 json={"flights": [params]})

        if response.status_code == 200:
            data = response.json()
            self.store_in_cache(params, data)
            return data
        else:
            print(
                f"API request failed with status code {response.status_code}")
            return None
