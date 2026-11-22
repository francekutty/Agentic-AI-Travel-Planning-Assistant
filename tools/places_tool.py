
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "places.json"


def load_places():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_places(city, place_type=None, min_rating=0):
    places = load_places()

    matching_places = [
        place for place in places
        if place["city"].strip().lower() == city.strip().lower()
        and (
            place_type is None
            or place["type"].strip().lower() == place_type.strip().lower()
        )
        and place["rating"] >= min_rating
    ]

    matching_places.sort(
        key=lambda place: place["rating"],
        reverse=True
    )

    return {
        "city": city,
        "place_type": place_type or "All",
        "minimum_rating": min_rating,
        "total_places": len(matching_places),
        "places": matching_places
    }


if __name__ == "__main__":
    result = search_places(
        city="Delhi",
        place_type=None,
        min_rating=4.0
    )

    print(json.dumps(result, indent=4))
