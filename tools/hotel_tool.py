
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "hotels.json"


def load_hotels():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_hotels(city, min_stars=0, max_price=None):
    hotels = load_hotels()

    matching_hotels = [
        hotel for hotel in hotels
        if hotel["city"].strip().lower() == city.strip().lower()
        and hotel["stars"] >= min_stars
        and (
            max_price is None
            or hotel["price_per_night"] <= max_price
        )
    ]

    matching_hotels.sort(
        key=lambda hotel: (
            -hotel["stars"],
            hotel["price_per_night"]
        )
    )

    return {
        "city": city,
        "total_hotels": len(matching_hotels),
        "hotels": matching_hotels
    }


if __name__ == "__main__":
    result = search_hotels(
        city="Delhi",
        min_stars=3,
        max_price=5000
    )

    print(json.dumps(result, indent=4))
