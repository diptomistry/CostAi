import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google Maps API key is missing. Check .env file.")

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Check .env file.")

genai.configure(api_key=GEMINI_API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

# Fetch current petrol cost
print("DEBUG: Sending request to Gemini API...")
response = model.generate_content([
  "input: current price per liter in CAD",
  "output: {\n \"current_price_per_liter\": \"1.71\",\n \"date\": \"2024-12-17\"\n}",
  "input: current price per liter in CAD", 
  "output: {\n \"current_price_per_liter\": \"1.70\",\n \"date\": \"2024-12-17\"\n}",
  "input: current price per liter in CAD",
  "output: {\n \"current_price_per_liter\": \"1.83\",\n \"date\": \"2024-12-17\"\n}",
  "input: ",
  "output: ",
])

# Debug: Print raw response
print("DEBUG: Raw Gemini API Response:")
print(response.text)

# Parse the price
try:
    # Attempt to parse the JSON
    cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
    price_data = json.loads(cleaned_text)
    
    # Debug: Print parsed data
    print("DEBUG: Parsed Price Data:")
    print(json.dumps(price_data, indent=2))
    
    CurrentPetrolCostCanada = float(price_data["current_price_per_liter"])
    
    # Debug: Print extracted price
    print(f"DEBUG: Extracted Price: ${CurrentPetrolCostCanada}")

except (json.JSONDecodeError, KeyError) as e:
    # Detailed error debugging
    print(f"DEBUG: Error parsing price - {type(e).__name__}: {e}")
    print(f"DEBUG: Problematic response text: {response.text}")
    
    # Fallback to a default price if parsing fails
    CurrentPetrolCostCanada = 1.7
    print("DEBUG: Falling back to default price")

# Vehicle types with dynamically calculated base rates
VEHICLE_TYPES = {
    "Car": {"base_rate": 5.8 * CurrentPetrolCostCanada, "fuel_efficiency": 14},  # km/l
    "Van": {"base_rate": 9.85 * CurrentPetrolCostCanada, "fuel_efficiency": 10},  # km/l
    "Pickup Truck": {"base_rate": 16.3 * CurrentPetrolCostCanada, "fuel_efficiency": 8},  # km/l
    "Tow Truck": {"base_rate": 25.2 * CurrentPetrolCostCanada, "fuel_efficiency": 6},  # km/l
    "Reefers (Refrigerated Truck)": {"base_rate": 32.5 * CurrentPetrolCostCanada, "fuel_efficiency": 5},  # km/l
    "Box Truck": {"base_rate": 39.49 * CurrentPetrolCostCanada, "fuel_efficiency": 7},  # km/l
    "Flatbed Truck": {"base_rate": 37.4 * CurrentPetrolCostCanada, "fuel_efficiency": 6}  # km/l
}

# Delivery categories remain the same
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

# Print the current petrol cost for verification
print(f"FINAL: Current Petrol Cost per Liter: ${CurrentPetrolCostCanada}")

# Example of how base rates are now dynamically calculated
for vehicle, details in VEHICLE_TYPES.items():
    print(f"{vehicle} Base Rate: ${details['base_rate']:.2f}")
'''
VEHICLE_TYPES = {
    "Car": {"base_rate": 7 * CurrentPetrolCostCanada, "fuel_efficiency": 15},  # km/l
    "Van": {"base_rate": 12 * CurrentPetrolCostCanada, "fuel_efficiency": 10},  # km/l
    "Pickup Truck": {"base_rate": 20 * CurrentPetrolCostCanada, "fuel_efficiency": 8},  # km/l
    "Tow Truck": {"base_rate": 30 * CurrentPetrolCostCanada, "fuel_efficiency": 6},  # km/l
    "Reefers (Refrigerated Truck)": {"base_rate": 40 * CurrentPetrolCostCanada, "fuel_efficiency": 5},  # km/l
    "Box Truck": {"base_rate": 35 * CurrentPetrolCostCanada, "fuel_efficiency": 7},  # km/l
    "Flatbed Truck": {"base_rate": 45 * CurrentPetrolCostCanada, "fuel_efficiency": 6}  # km/l
}
'''
# Vehicle types
# VEHICLE_TYPES = {
#     "Car": {"base_rate": 6.6 * CurrentPetrolCostCanada, "fuel_efficiency": 15},  # km/l
#     "Van": {"base_rate": 10.8 * CurrentPetrolCostCanada, "fuel_efficiency": 10},  # km/l
#     "Pickup Truck": {"base_rate": 18 * CurrentPetrolCostCanada, "fuel_efficiency": 8},  # km/l
#     "Tow Truck": {"base_rate": 27 * CurrentPetrolCostCanada, "fuel_efficiency": 6},  # km/l
#     "Reefers (Refrigerated Truck)": {"base_rate": 36 * CurrentPetrolCostCanada, "fuel_efficiency": 5},  # km/l
#     "Box Truck": {"base_rate": 31.5 * CurrentPetrolCostCanada, "fuel_efficiency": 7},  # km/l
#     "Flatbed Truck": {"base_rate": 40.5 * CurrentPetrolCostCanada, "fuel_efficiency": 6}  # km/l
# }