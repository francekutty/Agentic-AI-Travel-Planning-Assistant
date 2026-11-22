
import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city):
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=15
    )
    response.raise_for_status()

    results = response.json().get("results", [])

    if not results:
        raise ValueError(f"Location not found: {city}")

    location = results[0]

    return {
        "name": location["name"],
        "country": location.get("country", ""),
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    }


def get_weather_forecast(city, forecast_days=3):
    if not 1 <= forecast_days <= 7:
        raise ValueError("Forecast days must be between 1 and 7.")

    location = get_coordinates(city)

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max"
        ],
        "forecast_days": forecast_days,
        "timezone": "auto"
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=15
    )
    response.raise_for_status()

    weather_data = response.json()
    daily = weather_data.get("daily", {})

    forecast = []

    for i in range(len(daily.get("time", []))):
        forecast.append({
            "date": daily["time"][i],
            "weather_code": daily["weather_code"][i],
            "max_temperature": daily["temperature_2m_max"][i],
            "min_temperature": daily["temperature_2m_min"][i],
            "rain_probability": daily["precipitation_probability_max"][i]
        })

    return {
        "location": location,
        "forecast": forecast
    }


if __name__ == "__main__":
    try:
        result = get_weather_forecast("Delhi", 3)

        print("\nWEATHER FORECAST")
        print("-" * 40)
        print("Location:", result["location"]["name"])
        print("Country:", result["location"]["country"])

        for day in result["forecast"]:
            print("\nDate:", day["date"])
            print("Weather Code:", day["weather_code"])
            print("Maximum Temperature:", day["max_temperature"], "°C")
            print("Minimum Temperature:", day["min_temperature"], "°C")
            print("Rain Probability:", day["rain_probability"], "%")

    except (requests.RequestException, ValueError) as error:
        print("Weather Error:", error)
