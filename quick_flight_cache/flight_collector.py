from datetime import datetime


class FlightCollector:
    """
    A class to collect and manage flights grouped by date. This class allows adding, retrieving, and 
    filtering flights based on specific criteria.

    Attributes:
        flights (dict): A dictionary where each key is a date (str) and the value is a list of flights
                        for that date, following the structure of the API response.
    """

    def __init__(self):
        """
        Initializes an empty FlightCollector with a dictionary to store flights organized by date.
        """
        self.flights = {}

    def add_flights(self, date, flights_data):
        """
        Adds a list of flights for a specific date to the collection. If flights already exist for that
        date, the new flights are appended.

        Parameters:
            date (str): The date of the flights in 'YYYY-MM-DD' format.
            flights_data (list): A list of flights for the specified date. Each flight should be in the
                                 format provided by the API response.
        """
        if date not in self.flights:
            self.flights[date] = []
        self.flights[date].extend(flights_data)

    def get_all_flights(self):
        """
        Retrieves all flights across all dates in the collection.

        Returns:
            list: A list of all flights, regardless of the date, combined into a single list.
        """
        all_flights = []
        for date, flights in self.flights.items():
            all_flights.extend(flights)
        return all_flights

    def get_flights_by_date(self, date):
        """
        Retrieves all flights for a specific date.

        Parameters:
            date (str): The date for which to retrieve flights, in 'YYYY-MM-DD' format.

        Returns:
            list: A list of flights for the specified date. If no flights exist for the date, an empty list is returned.
        """
        return self.flights.get(date, [])

    def filter_flights(self, filter_func):
        """
        Filters flights across all dates based on a specified filter function.

        Parameters:
            filter_func (function): A function that takes a flight (dict) as input and returns True if the
                                    flight meets the filtering criteria, or False otherwise.

        Returns:
            list: A list of flights that match the criteria defined by the filter function.
        """
        filtered_flights = []
        for flights in self.flights.values():
            filtered_flights.extend(filter(filter_func, flights))
        return filtered_flights
