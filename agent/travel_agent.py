
from langchain.agents import create_agent
from langchain.tools import tool

from agent.llm_setup import llm

from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import search_places
from tools.weather_tool import get_weather_forecast
from tools.budget_tool import calculate_budget


# TOOL 1: Flight Search
@tool
def flight_search(source: str, destination: str, sort_by: str = "cheapest"):
    """Search flights between two cities. Sort by cheapest or fastest."""
    return search_flights(source, destination, sort_by)


# TOOL 2: Hotel Search
@tool
def hotel_search(city: str, min_stars: int = 0, max_price: int = None):
    """Find hotels in a city using minimum star rating and maximum nightly price."""
    return search_hotels(city, min_stars, max_price)


# TOOL 3: Places Search
@tool
def places_search(city: str, place_type: str = None, min_rating: float = 0):
    """Find tourist attractions in a city, filtered by type and minimum rating."""
    return search_places(city, place_type, min_rating)


# TOOL 4: Weather Forecast
@tool
def weather_search(city: str, forecast_days: int = 3):
    """Get the live weather forecast for a city for the next 1 to 7 days."""
    return get_weather_forecast(city, forecast_days)


# TOOL 5: Budget Calculation
@tool
def budget_estimator(
    flight_price: float,
    hotel_price_per_night: float,
    trip_days: int,
    daily_expenses: float = 1500
):
    """Estimate flight, hotel and local expenses in INR."""
    return calculate_budget(
        flight_price,
        hotel_price_per_night,
        trip_days,
        daily_expenses
    )


# Register all five tools
travel_tools = [
    flight_search,
    hotel_search,
    places_search,
    weather_search,
    budget_estimator
]


# Create the Agentic AI travel assistant
travel_agent = create_agent(
    model=llm,
    tools=travel_tools,
    system_prompt="""
    You are an intelligent Agentic AI Travel Planning Assistant.

    Understand the user's travel requirements and use the available
    tools to search flights, hotels, tourist attractions, weather
    and estimated budgets.

    Requirements:
    1. Identify source city and destination city.
    2. Compare cheapest and fastest flights when useful.
    3. Recommend suitable hotels based on price and rating.
    4. Suggest attractions based on city, type and rating.
    5. Retrieve weather forecasts for the destination.
    6. Calculate the estimated trip budget.
    7. Generate a practical day-wise itinerary for 3 to 7 days.
    8. Provide a trip summary and budget breakdown.
    9. Explain your recommendations briefly.
    10. Never invent flight, hotel or attraction records.

    Important:
    - Flight, hotel and attraction results come from local JSON datasets.
    - Do not describe those results as real-time availability.
    - Weather comes from the Open-Meteo API.
    - Clearly disclose unavailable information.
    - Flight prices are the listed dataset prices; do not assume
      they include return journeys.
    - Budget estimates must state their assumptions.
    - Return both readable information and a JSON-style summary.
    """
)


if __name__ == "__main__":
    print("\nAGENTIC AI TRAVEL PLANNER")
    print("=" * 45)

    query = """
    Plan a 3-day trip from Hyderabad to Delhi.
    Find the cheapest flight, a suitable hotel,
    popular tourist attractions, weather forecast
    and estimated total budget.
    Create a day-wise itinerary.
    """

    response = travel_agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    print("\nTRAVEL PLAN")
    print("=" * 45)

    print(response["messages"][-1].content)
