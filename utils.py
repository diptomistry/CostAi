import requests
from fastapi import HTTPException
from config import VEHICLE_TYPES, DELIVERY_CATEGORIES, GOOGLE_API_KEY, CurrentPetrolCostCanada

def calculate_cost(pickup_address, delivery_address, vehicle_type, delivery_category):
    # Validate vehicle type
    if vehicle_type not in VEHICLE_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid vehicle type. Choose from: {list(VEHICLE_TYPES.keys())}")

    # Validate delivery category
    category_modifier = DELIVERY_CATEGORIES.get(delivery_category, 1.0)

    # Google Maps Distance Matrix API
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": pickup_address,
        "destinations": delivery_address,
        "key": GOOGLE_API_KEY,
    }

    try:
        # Fetch distance data
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            raise HTTPException(status_code=400, detail="Error fetching distance data")

        distance_text = data["rows"][0]["elements"][0]["distance"]["text"]
        distance_value = data["rows"][0]["elements"][0]["distance"]["value"]  # in meters
        distance_km = distance_value / 1000  # Convert meters to kilometers

        # Calculate cost per kilometer
        vehicle = VEHICLE_TYPES[vehicle_type]
        base_rate = vehicle["base_rate"]
        fuel_efficiency = vehicle["fuel_efficiency"]
        fuel_cost_per_km = CurrentPetrolCostCanada / fuel_efficiency
        cost_per_km = (base_rate + fuel_cost_per_km) * category_modifier

        # Calculate total cost
        delivery_cost = round(distance_km * cost_per_km, 2)

        return {
            "distance": distance_text,
            "cost_per_km": f"${round(cost_per_km, 2)}",
            "total_cost": f"${delivery_cost}",
            "delivery_category_modifier": category_modifier
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
