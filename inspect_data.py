
import json
import os

files = ["flights.json", "hotels.json", "places.json"]

for filename in files:
    print(f"\n{'=' * 50}")
    print(f"DATASET: {filename}")
    print("=" * 50)

    if not os.path.exists(filename):
        print("File not found!")
        continue

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        print("Total records:", len(data))
        if data:
            print("Available fields:", list(data[0].keys()))
            print("Sample record:", data[0])

    elif isinstance(data, dict):
        print("Top-level keys:", list(data.keys()))
        print("Sample data:", str(data)[:1000])

    else:
        print("Data type:", type(data))
