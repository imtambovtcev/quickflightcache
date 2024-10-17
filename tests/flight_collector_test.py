from quick_flight_cache import FlightCollector
import pytest
from datetime import datetime

# Sample flight data
sample_flight_nov_26 = [
    {'id': 'flight1', 'price': {'raw': 120.0}, 'legs': [], 'date': '2024-11-26'},
    {'id': 'flight2', 'price': {'raw': 200.0}, 'legs': [], 'date': '2024-11-26'}
]
sample_flight_nov_27 = [
    {'id': 'flight3', 'price': {'raw': 95.0}, 'legs': [], 'date': '2024-11-27'}
]

# Initialize the FlightCollector class for testing


@pytest.fixture
def flight_collector():
    return FlightCollector()


def test_add_flights(flight_collector):
    flight_collector.add_flights("2024-11-26", sample_flight_nov_26)
    assert len(flight_collector.get_flights_by_date("2024-11-26")) == 2


def test_get_all_flights(flight_collector):
    flight_collector.add_flights("2024-11-26", sample_flight_nov_26)
    flight_collector.add_flights("2024-11-27", sample_flight_nov_27)
    assert len(flight_collector.get_all_flights()) == 3


def test_get_flights_by_date(flight_collector):
    flight_collector.add_flights("2024-11-26", sample_flight_nov_26)
    flights_nov_26 = flight_collector.get_flights_by_date("2024-11-26")
    assert len(flights_nov_26) == 2
    assert flights_nov_26[0]['id'] == 'flight1'
    assert flights_nov_26[1]['id'] == 'flight2'


def test_filter_flights(flight_collector):
    flight_collector.add_flights("2024-11-26", sample_flight_nov_26)
    flight_collector.add_flights("2024-11-27", sample_flight_nov_27)
    # Filter for flights with price < 150
    cheap_flights = flight_collector.filter_flights(
        lambda flight: flight['price']['raw'] < 150)
    assert len(cheap_flights) == 2
    assert cheap_flights[0]['id'] == 'flight1'
    assert cheap_flights[1]['id'] == 'flight3'
