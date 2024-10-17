# QuickFlightCache

![logo](image/README/logo.png)

QuickFlightCache is a Python package designed for quick and efficient flight search using the RapidAPI platform, with added functionality to cache responses to minimize API calls and reduce response times for repeated requests. It simplifies retrieving flights, filtering results, and displaying flight details.

## Features

- **RapidAPI Integration**: Seamlessly connects to the RapidAPI Skyscanner API.
- **Caching System**: Stores search results locally, reducing API call count.
- **Flight Management**: Collect flights for multiple dates and filter results.
- **Readable Flight Information**: Formats and displays flight details, including layover times.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/imtambovtcev/quickflightcache.git
    ```
2. Navigate to the project folder and install dependencies using Poetry:
    ```bash
    cd quickflightcache
    poetry install
    ```

## Usage

### Initial Setup

Import the required classes from QuickFlightCache:

```python
from quick_flight_cache import FlightSearch, FlightCollector, display_flights
```

### 1. Selecting Airports

Use RapidAPI to find the airport codes (Entity IDs) for departure and destination locations. For example, you can retrieve codes for **Keflavík International Airport** in Iceland (`KEF`) and **Antalya Airport** in Turkey (`AYT`). 

The airport codes are crucial for making accurate flight searches with the `FlightSearch` class.


### 2. Initialize the `FlightSearch` instance

QuickFlightCache uses the [Sky Scanner API](https://rapidapi.com/ntd119/api/sky-scanner3) on RapidAPI. To get started, provide your RapidAPI credentials and specify caching options:

```python
flight_search = FlightSearch(
    api_key="your_rapidapi_key",  # RapidAPI key from your Sky Scanner subscription
    api_host="sky-scanner3.p.rapidapi.com",
    cache_file="flight_cache.json",
    cache_expiry_days=1  # Optional, default is 1 day
)
```


### 3. Search Flights and Add to Collector

Specify dates and search flights for each date, adding results to the `FlightCollector`:
```python
collector = FlightCollector()
dates = ["2024-11-30", "2024-12-01", "2024-12-02"]

for date in dates:
    result = flight_search.search_flights(
        fromEntityId="KEF",
        toEntityId="AYT",
        departDate=date,
        update_cache=False
    )

    flights = result.get('data', {}).get('itineraries', [])
    if flights:
        print(f"{len(flights)} flights found for {date}")
        collector.add_flights(date, flights)
    else:
        print(f"No flights found for {date}")
```

### 4. Retrieve and Filter Flights

Retrieve all flights or filter them based on custom criteria. For instance, filtering for flights under $150:

```python
all_flights = collector.get_all_flights()
cheap_flights = collector.filter_flights(lambda flight: flight['price']['raw'] < 150)

print("All flights collected:", all_flights)
print("Filtered cheap flights:", cheap_flights)
```

### 5. Display Flights

Using the `display_flights` function to format and display detailed information for each flight:

```python
display_flights(all_flights)
```

### Sample Output

When you run `display_flights(all_flights)`, the output will be formatted as follows:

```
Price: $345
Duration: 8h 30m
Stops: 1
Departure: Nov 30, 2024 - 3:00 PM
Arrival: Nov 30, 2024 - 11:30 PM

Segments:
  KEF -> FRA
    Airline: Icelandair
    Departure: Nov 30, 2024 - 3:00 PM
    Arrival: Nov 30, 2024 - 7:30 PM

    Layover: 2h 15m

  FRA -> AYT
    Airline: SunExpress
    Departure: Nov 30, 2024 - 9:45 PM
    Arrival: Nov 30, 2024 - 11:30 PM
========================================
```

## Caching Strategy

QuickFlightCache automatically checks cached responses based on request parameters. To refresh the cache, set `update_cache=True` in the `search_flights` method.