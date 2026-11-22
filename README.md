# Agentic AI-Based Travel Planning Assistant Using LangChain

## Project Overview
The Agentic AI-Based Travel Planning Assistant is an intelligent travel planning application developed using LangChain, Google Gemini and Streamlit.

The system understands user travel requirements, selects appropriate tools, retrieves travel information, estimates expenses and generates personalized day-wise itineraries.

## Objectives
- Search flights based on source and destination.
- Recommend hotels based on city, rating and price.
- Suggest tourist attractions based on location, category and rating.
- Retrieve real-time weather forecasts using Open-Meteo API.
- Estimate total travel expenses.
- Generate structured JSON and human-readable travel plans.

## Technologies Used
- Python
- LangChain
- Google Gemini API
- Streamlit
- Open-Meteo API
- JSON
- Requests
- Python-dotenv

## Project Structure
```text
agentic_ai_travel_planner/
│
├── agent/
│   ├── __init__.py
│   ├── llm_setup.py
│   └── travel_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── flight_tool.py
│   ├── hotel_tool.py
│   ├── places_tool.py
│   ├── weather_tool.py
│   └── budget_tool.py
│
├── flights.json
├── hotels.json
├── places.json
├── app.py
├── inspect_data.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

## Main Features

### 1. Flight Search
Searches flights between two cities and supports cheapest and fastest flight selection.

### 2. Hotel Recommendation
Filters hotels using city, minimum star rating and maximum price per night.

### 3. Tourist Places
Recommends attractions based on city, place type and minimum rating.

### 4. Weather Forecast
Uses the Open-Meteo API to retrieve weather forecasts.

### 5. Budget Estimation
Calculates flight expenses, hotel expenses and daily local expenses.

### 6. Agentic AI
Uses LangChain and Google Gemini to understand user queries and decide which tools to invoke.

### 7. Streamlit Interface
Provides an interactive interface for entering travel preferences and viewing generated travel plans.

### 8. Structured Output
Displays human-readable itineraries and JSON travel summaries.

## Installation and Execution

1. Clone or download the project.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your Google Gemini API key in `.env`:

```env
GOOGLE_API_KEY=your_api_key
```

5. Run the application:

```bash
streamlit run app.py
```

## Data Sources
- Flights: flights.json
- Hotels: hotels.json
- Tourist attractions