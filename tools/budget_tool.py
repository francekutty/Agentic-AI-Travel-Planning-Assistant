
def calculate_budget(
    flight_price,
    hotel_price_per_night,
    trip_days,
    daily_expenses=1500
):
    if flight_price < 0 or hotel_price_per_night < 0:
        raise ValueError("Prices cannot be negative.")

    if trip_days < 1:
        raise ValueError("Trip duration must be at least one day.")

    if daily_expenses < 0:
        raise ValueError("Daily expenses cannot be negative.")

    # A trip of 3 days normally requires 2 hotel nights
    hotel_nights = trip_days - 1

    flight_cost = flight_price
    hotel_cost = hotel_price_per_night * hotel_nights
    local_expenses = daily_expenses * trip_days

    total_budget = flight_cost + hotel_cost + local_expenses

    return {
        "flight_cost": flight_cost,
        "hotel_cost": hotel_cost,
        "hotel_nights": hotel_nights,
        "daily_local_expenses": daily_expenses,
        "trip_days": trip_days,
        "local_expenses_total": local_expenses,
        "total_budget": total_budget,
        "currency": "INR"
    }


if __name__ == "__main__":
    result = calculate_budget(
        flight_price=2907,
        hotel_price_per_night=3897,
        trip_days=3,
        daily_expenses=1500
    )

    print("\nTRIP BUDGET ESTIMATION")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")
