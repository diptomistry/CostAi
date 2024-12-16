from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google Maps API key is missing. Check .env file.")

# Current petrol cost
CurrentPetrolCostCanada = 1.5

# Vehicle types
VEHICLE_TYPES = {
    "Car": {"base_rate": 7 * CurrentPetrolCostCanada, "fuel_efficiency": 15},  # km/l
    "Van": {"base_rate": 12 * CurrentPetrolCostCanada, "fuel_efficiency": 10},  # km/l
    "Pickup Truck": {"base_rate": 20 * CurrentPetrolCostCanada, "fuel_efficiency": 8},  # km/l
    "Tow Truck": {"base_rate": 30 * CurrentPetrolCostCanada, "fuel_efficiency": 6},  # km/l
    "Reefers (Refrigerated Truck)": {"base_rate": 40 * CurrentPetrolCostCanada, "fuel_efficiency": 5},  # km/l
    "Box Truck": {"base_rate": 35 * CurrentPetrolCostCanada, "fuel_efficiency": 7},  # km/l
    "Flatbed Truck": {"base_rate": 45 * CurrentPetrolCostCanada, "fuel_efficiency": 6}  # km/l
}

# Delivery categories
DELIVERY_CATEGORIES = {
    "MEDICINE": 0.6,
    "GROCERY DELIVERY": 0.9,
    "FOOD DELIVERY": 1.0,
    "CAR PARTS": 1.2,
    "TORONTO LAB": 1.3,
    "SENIOR (PACKAGE PICKUP)": 0.8,
    "SENIOR APPOINTMENT": 1.1,
    "CANNABIS DELIVERY": 1.2,
    "PICKUP TRUCK": 1.0,
    "VAN DELIVERY": 1.0,
    "STANDARD DELIVERY": 1.0,
    "FLOWER DELIVERY": 1.1,
    "CAR": 1.0
}
