
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
def flight_search(
    source: str,
    destination: str,
    sort_by: str = "cheapest"
):
    """Search flights between two cities. Sort by cheapest or fastest."""

    return search_flights(source, destination, sort_by)


# TOOL 2: Hotel Search
@tool
def hotel_search(
    city: str,
    min_stars: int = 0,
    max_price: int = None
):
    """Find hotels using city, minimum star rating and maximum nightly price."""

    return search_hotels(city, min_stars, max_price)


# TOOL 3: Places Search
@tool
def places_search(
    city: str,
    place_type: str = None,
    min_rating: float = 0
):
    """Find tourist attractions using city, type and minimum rating."""

    return search_places(city, place_type, min_rating)


# TOOL 4: Weather Forecast
@tool
def weather_search(
    city: str,
    forecast_days: int = 3
):
    """Retrieve weather forecasts for a destination for 1 to 7 days."""

    forecast_days = max(1, min(forecast_days, 7))

    return get_weather_forecast(city, forecast_days)


# TOOL 5: Budget Calculation
@tool
def budget_estimator(
    flight_price: float,
    hotel_price_per_night: float,
    trip_days: int,
    daily_expenses: float = 1500
):
    """Calculate estimated flight, accommodation and local expenses in INR."""

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

Your responsibility is to plan practical and personalized trips
using the available tools.

AGENT WORKFLOW:

1. Understand the user's source city, destination city,
   trip duration, budget and preferences.

2. FLIGHT SEARCH:
   - Use flight_search to find the cheapest flight.
   - Use flight_search again to find the fastest flight.
   - Compare the available results.
   - Recommend the most suitable option.
   - Use only actual flight records returned by the tool.

3. HOTEL RECOMMENDATION:
   - Use hotel_search for the destination city.
   - Apply the user's minimum star rating and maximum price.
   - Compare available hotels.
   - Recommend a suitable hotel using actual returned records.

4. PLACES DISCOVERY:
   - Use places_search for the destination city.
   - Recommend attractions based on their type and rating.
   - Use only attractions returned by the dataset.
   - If no matching attractions are found, clearly say so.
   - Never replace missing dataset results with famous attractions
     from your general knowledge.

5. WEATHER:
   - Use weather_search for the destination city.
   - Request a forecast matching the trip duration, up to 7 days.
   - Report the actual weather information returned by the API.
   - Never invent weather conditions.

6. BUDGET ESTIMATION:
   - Use budget_estimator with the selected flight price,
     hotel price per night and trip duration.
   - Include daily local expenses.
   - Clearly explain the budget assumptions.
   - Do not assume flight prices include return journeys.
   - Compare the estimated total against the user's budget.

7. ITINERARY:
   - Generate a practical day-wise itinerary for 3 to 7 days.
   - Use available attractions from places_search.
   - Distribute attractions across the trip days.
   - Do not invent attractions when dataset results are unavailable.

8. DECISION EXPLANATION:
   - Briefly explain why the flight and hotel were selected.
   - Explain how price, rating and user preferences influenced
     the recommendations.

IMPORTANT RULES:

- Flights, hotels and places must come from the supplied JSON datasets.
- Preserve the correct city and location information.
- Do not claim real-time flight or hotel booking availability.
- Weather must come from the Open-Meteo API.
- Clearly report unavailable information.
- Never fabricate dataset records, prices, ratings or weather.
- Do not claim that a tool was used unless it was actually called.

FINAL RESPONSE FORMAT:

1. Trip Summary
2. Flight Options and Selected Flight
3. Hotel Recommendation
4. Places to Visit
5. Weather Forecast
6. Day-wise Itinerary
7. Budget Breakdown
8. Reasoning Behind Recommendations

Provide clear, readable and structured information.
"""
)


# Test the agent independently
if __name__ == "__main__":

    print("\nAGENTIC AI TRAVEL PLANNER")
    print("=" * 50)

    query = """
    Plan a 3-day trip from Hyderabad to Delhi.

    Find the cheapest and fastest flights.
    Recommend a hotel with at least 3 stars.
    Find highly rated tourist attractions.
    Get the weather forecast for all 3 days.
    Calculate the complete estimated budget.

    Create a day-wise itinerary and explain your decisions.
    Use the available tools and actual dataset records.
    """

    response = travel_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })

    print("\nFINAL TRAVEL PLAN")
    print("=" * 50)

    print(response["messages"][-1].content)

    print("\nAGENT TOOL USAGE")
    print("=" * 50)

    for message in response["messages"]:
        if hasattr(message, "tool_calls") and message.tool_calls:
            for call in message.tool_calls:
                print("Tool called:", call["name"])
