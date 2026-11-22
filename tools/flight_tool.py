
import json
from pathlib import Path
from datetime import datetime, timedelta

# Locate flights.json in the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "flights.json"


def load_flights():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_duration(departure, arrival):
    departure_time = datetime.fromisoformat(departure)
    arrival_time = datetime.fromisoformat(arrival)

    # Handle flights arriving on the next day
    if arrival_time < departure_time:
        arrival_time += timedelta(days=1)

    return (arrival_time - departure_time).total_seconds() / 60


def search_flights(source, destination, sort_by="cheapest"):
    flights = load_flights()

    matching_flights = [
        flight for flight in flights
        if flight["from"].strip().lower() == source.strip().lower()
        and flight["to"].strip().lower() == destination.strip().lower()
    ]

    if not matching_flights:
        return {
            "message": "No flights found for this route.",
            "flights": []
        }

    if sort_by.lower() == "cheapest":
        matching_flights.sort(key=lambda flight: flight["price"])

    elif sort_by.lower() == "fastest":
        matching_flights.sort(
            key=lambda flight: calculate_duration(
                flight["departure_time"],
                flight["arrival_time"]
            )
        )

    else:
        return {
            "message": "Invalid sorting option. Use cheapest or fastest.",
            "flights": []
        }

    return {
        "source": source,
        "destination": destination,
        "sort_by": sort_by,
        "total_flights": len(matching_flights),
        "flights": matching_flights
    }


if __name__ == "__main__":
    result = search_flights("Hyderabad", "Delhi", "cheapest")
    print(json.dumps(result, indent=4))
