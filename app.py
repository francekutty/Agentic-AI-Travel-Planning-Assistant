from json_repair import repair_json
import json
import streamlit as st

from agent.llm_setup import llm
from agent.travel_agent import travel_agent


def content_to_text(content):
    """Convert an LLM response into plain text."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict):
                text_part = item.get("text", "")

                if text_part:
                    parts.append(text_part)

            elif isinstance(item, str):
                parts.append(item)

        return "\n".join(parts)

    return str(content)



def convert_to_json(travel_plan):
    prompt = f"""
    Convert the following travel plan into valid JSON.

    Return ONLY a JSON object.
    Do not include Markdown, explanations, or code fences.
    Use double quotes for all property names and string values.
    Use numbers for numeric values.
    Use empty arrays [] when information is unavailable.
    
    Required structure:
    {{
        "trip_summary": {{
            "source": "",
            "destination": "",
            "duration_days": 0
        }},
        "flight_recommendation": {{}},
        "hotel_recommendation": {{}},
        "places_to_visit": [],
        "weather_forecast": [],
        "day_wise_itinerary": [],
        "budget_breakdown": {{
            "flight_cost": 0,
            "hotel_cost": 0,
            "local_expenses": 0,
            "total_budget": 0
        }}
    }}

    Travel plan:
    {travel_plan}
    """

    response = llm.invoke(prompt)
    content = response.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )

    content = content.strip()

    return json.loads(repair_json(content))



st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Agentic AI Travel Planning Assistant")
st.write("Plan your journey with the power of Agentic AI.")

st.divider()

st.subheader("Enter Your Travel Details")

with st.form("travel_form"):

    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input(
            "Source City",
            placeholder="e.g. Hyderabad"
        )

        destination = st.text_input(
            "Destination City",
            placeholder="e.g. Delhi"
        )

        trip_days = st.slider(
            "Trip Duration (Days)", 3, 7, 3
        )

    with col2:
        budget = st.number_input(
            "Maximum Budget (INR)",
            min_value=1000,
            value=20000,
            step=1000
        )

        hotel_price = st.number_input(
            "Maximum Hotel Price Per Night (INR)",
            min_value=500,
            value=5000,
            step=500
        )

        min_stars = st.selectbox(
            "Minimum Hotel Rating",
            [0, 2, 3, 4, 5],
            index=2
        )

    submitted = st.form_submit_button(
        "Generate My Travel Plan",
        use_container_width=True
    )


if submitted:

    if not source.strip() or not destination.strip():

        st.error("Please enter both source and destination cities.")

    elif source.strip().lower() == destination.strip().lower():

        st.error("Source and destination must be different.")

    else:

        query = f"""
        Plan a {trip_days}-day trip from {source} to {destination}.

        Maximum total budget: INR {budget}.
        Maximum hotel price per night: INR {hotel_price}.
        Minimum hotel star rating: {min_stars}.

        Use the available tools to:

        1. Find and compare the cheapest and fastest flights.
        2. Recommend suitable hotels within the hotel price limit.
        3. Find highly rated tourist attractions.
        4. Get the destination's weather forecast.
        5. Estimate the complete trip budget.
        6. Create a day-wise itinerary.

        Explain your recommendations.

        Do not invent dataset records or claim live booking availability.
        Clearly state if the estimated budget exceeds my maximum budget.
        """

        with st.spinner(
            "Your AI travel agent is planning your trip..."
        ):

            try:

                # Generate human-readable travel plan
                response = travel_agent.invoke({
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                })

                answer = content_to_text(
                    response["messages"][-1].content
                )

                # Generate structured JSON
                json_prompt = f"""
                Convert the travel plan below into one valid JSON object.

                Follow this exact structure:

                {{
                    "trip_summary": {{
                        "source": "{source}",
                        "destination": "{destination}",
                        "duration_days": {trip_days}
                    }},
                    "flight_recommendation": "",
                    "hotel_recommendation": "",
                    "places_to_visit": [],
                    "weather_forecast": [],
                    "day_wise_itinerary": [],
                    "budget_breakdown": {{
                        "flight_cost": null,
                        "hotel_cost": null,
                        "local_expenses": null,
                        "total_budget": null
                    }}
                }}

                Travel plan:
                {answer}

                Rules:
                - Return only a valid JSON object.
                - Do not use Markdown code fences.
                - Do not add explanations outside the JSON.
                - Do not invent missing information.
                - Use null or empty arrays when information is unavailable.
                """

                json_response = llm.invoke(json_prompt)

                # Convert response into JSON
                try:

                    structured_data = convert_to_json(
                        json_response.content
                    )

                except (json.JSONDecodeError, TypeError, ValueError) as json_error:

                    st.warning(
                        "The travel plan was generated, but its "
                        "structured JSON conversion failed."
                    )

                    st.caption(f"JSON conversion detail: {json_error}")

                    structured_data = {
                        "trip_summary": {
                            "source": source,
                            "destination": destination,
                            "duration_days": trip_days
                        },
                        "json_conversion_error": str(json_error),
                        "travel_plan": answer
                    }

                # Display human-readable result
                st.success("Your travel plan is ready!")

                st.subheader("🌍 Your AI-Generated Travel Plan")
                st.markdown(answer)

                # Display structured JSON
                st.divider()

                st.subheader("📦 Structured JSON Output")
                st.json(structured_data)

                # Download JSON
                st.download_button(
                    label="Download Travel Plan JSON",
                    data=json.dumps(
                        structured_data,
                        indent=4,
                        ensure_ascii=False
                    ),
                    file_name="travel_plan.json",
                    mime="application/json"
                )

            except Exception as error:

                st.error(
                    f"Unable to generate travel plan: {error}"
                )
