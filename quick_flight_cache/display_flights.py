from datetime import datetime


def display_flights(flights):
    """
    Displays flight details in a human-readable format, including price, duration, stops, departure and 
    arrival times, and segment information. Also calculates and displays layover times between segments.

    Parameters:
        flights (list): A list of flight dictionaries, where each dictionary follows the structure 
                        of the API response. Each flight dictionary should contain information on
                        price, legs, segments, and carrier details.

    Returns:
        None
    """
    for flight in flights:
        # Extract main flight details
        price = flight['price']['formatted']
        duration = flight['legs'][0]['durationInMinutes']
        stops = flight['legs'][0]['stopCount']

        # Convert departure and arrival times to human-readable format
        departure = datetime.fromisoformat(
            flight['legs'][0]['departure']).strftime("%b %d, %Y - %I:%M %p")
        arrival = datetime.fromisoformat(
            flight['legs'][0]['arrival']).strftime("%b %d, %Y - %I:%M %p")

        # Display general flight information
        print(f"Price: {price}")
        print(f"Duration: {duration // 60}h {duration % 60}m")
        print(f"Stops: {stops}")
        print(f"Departure: {departure}")
        print(f"Arrival: {arrival}")

        # Display each segment and calculate layover times if there are multiple segments
        print("\nSegments:")
        segments = flight['legs'][0]['segments']
        for i, segment in enumerate(segments):
            origin = segment['origin']['displayCode']
            destination = segment['destination']['displayCode']

            # Format segment departure and arrival times for readability
            departure_time = datetime.fromisoformat(
                segment['departure']).strftime("%b %d, %Y - %I:%M %p")
            arrival_time = datetime.fromisoformat(
                segment['arrival']).strftime("%b %d, %Y - %I:%M %p")
            airline = segment['marketingCarrier']['name']

            print(f"  {origin} -> {destination}")
            print(f"    Airline: {airline}")
            print(f"    Departure: {departure_time}")
            print(f"    Arrival: {arrival_time}")

            # Calculate layover duration between segments
            if i < len(segments) - 1:
                next_departure = segments[i + 1]['departure']
                # Convert to datetime objects for calculation
                arrival_dt = datetime.fromisoformat(segment['arrival'])
                next_departure_dt = datetime.fromisoformat(next_departure)
                # Calculate layover time
                layover_duration = next_departure_dt - arrival_dt
                hours, remainder = divmod(
                    layover_duration.total_seconds(), 3600)
                minutes = remainder // 60
                print(f"\n    Layover: {int(hours)}h {int(minutes)}m\n")

        print("=" * 40)  # Separator between flights
