import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# File to store the petrol cost
PETROL_COST_FILE = "petrol_cost.json"

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
    "temperature": 0,  # Makes the response deterministic
    "top_p": 1,        # Disable nucleus sampling (1 means no cutoff)
    "top_k": 1,        # Choose the single most probable token
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def fetch_petrol_cost():
    """Fetch current petrol cost using Gemini API."""
    print("Fetching current petrol cost from Gemini API...")
    response = model.generate_content([
    "You are an intelligent assistant for logistics and delivery applications. Your role is to determine the current price per liter of petrol in CAD for Canada. Provide the current price per liter of petrol/gasoline in CAD.Follow the input output for the response format but provide the actual currrent rate.",
    "input: current price per liter in CAD",
    "output: {\n    \"current_price_per_liter\": \"1.65\",\n    \"date\": \"2024-11-17\"\n}",
    "input: ",
    "output: ",
    ])

    try:
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        price_data = json.loads(cleaned_text)
        price_str = price_data.get("current_price_per_liter", "1.7")
        petrol_cost = float(price_str)
        return {"current_price_per_liter": petrol_cost, "date": datetime.now().strftime("%Y-%m-%d")}
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        print(f"Error fetching price: {e}")
        return {"current_price_per_liter": 1.7, "date": datetime.now().strftime("%Y-%m-%d")}  # Fallback value

def get_petrol_cost():
    """Get petrol cost from file or fetch new cost if outdated."""
    if os.path.exists(PETROL_COST_FILE):
        with open(PETROL_COST_FILE, "r") as file:
            data = json.load(file)
            if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                print("Loaded petrol cost from file.")
                print(f"DEBUG: Current Petrol Cost per Liter: ${data['current_price_per_liter']}")
                return data["current_price_per_liter"]

    # If the file is missing or outdated, fetch new data
    petrol_data = fetch_petrol_cost()
    with open(PETROL_COST_FILE, "w") as file:
        json.dump(petrol_data, file, indent=2)
    print("Updated petrol cost and saved to file.")
    return petrol_data["current_price_per_liter"]

# Get today's petrol cost
ConstCurrentPetrolCostCanada = get_petrol_cost()
#ConstCurrentPetrolCostCanada=1.5
# Vehicle types with dynamically calculated base rates
VEHICLE_TYPES = {
    "Car": {"base_rate": 6.2 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 14},
    "Van": {"base_rate": 9.85 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 10},
    "Pickup Truck": {"base_rate": 16.3 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 8},
    "Tow Truck": {"base_rate": 25.2 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 6},
    "Reefers (Refrigerated Truck)": {"base_rate": 32.5 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 5},
    "Box Truck": {"base_rate": 39.49 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 7},
    "Flatbed Truck": {"base_rate": 37.4 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 6},
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
    "CAR": 1.0,
}

# Print the current petrol cost for verification
print(f"FINAL: Current Petrol Cost per Liter: ${ConstCurrentPetrolCostCanada}")

# Example of how base rates are now dynamically calculated
for vehicle, details in VEHICLE_TYPES.items():
    print(f"{vehicle} Base Rate: ${details['base_rate']:.2f}")


'''
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
  "You are an intelligent assistant for logistics and delivery applications. Your role is to determine the current price per liter of petrol in CAD for Canada. Provide the current price per liter of petrol/gasoline in CAD.Follow the input output for the response format but provide the actual currrent rate.",
  "input: current price per liter in CAD",
  "output: {\n    \"current_price_per_liter\": \"1.65\",\n    \"date\": \"2024-11-17\"\n}",
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
    
    price_str = price_data.get("current_price_per_liter", "Unavailable")
    try:
        CurrentPetrolCostCanada = float(price_str)
    except ValueError:
        print(f"DEBUG: Invalid price received: {price_str}")
        CurrentPetrolCostCanada = 1.7  # Fallback to default price
    
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
ConstCurrentPetrolCostCanada = CurrentPetrolCostCanada 
#ConstCurrentPetrolCostCanada = 1.5
VEHICLE_TYPES = {
    "Car": {"base_rate": 5.8 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 14},  # km/l
    "Van": {"base_rate": 9.85 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 10},  # km/l
    "Pickup Truck": {"base_rate": 16.3 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 8},  # km/l
    "Tow Truck": {"base_rate": 25.2 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 6},  # km/l
    "Reefers (Refrigerated Truck)": {"base_rate": 32.5 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 5},  # km/l
    "Box Truck": {"base_rate": 39.49 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 7},  # km/l
    "Flatbed Truck": {"base_rate": 37.4 * ConstCurrentPetrolCostCanada, "fuel_efficiency": 6}  # km/l
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
print(f"FINAL: Current Petrol Cost per Liter: ${ConstCurrentPetrolCostCanada}")

# Example of how base rates are now dynamically calculated
for vehicle, details in VEHICLE_TYPES.items():
    print(f"{vehicle} Base Rate: ${details['base_rate']:.2f}")
'''






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





# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Google API key
# GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
# if not GOOGLE_API_KEY:
#     raise ValueError("Google Maps API key is missing. Check .env file.")

# # Current petrol cost
# CurrentPetrolCostCanada = 1.71

# VEHICLE_TYPES = {
#     "Car": {"base_rate": 5.8 * CurrentPetrolCostCanada, "fuel_efficiency": 14},  # km/l
#     "Van": {"base_rate": 9.85 * CurrentPetrolCostCanada, "fuel_efficiency": 10},  # km/l
#     "Pickup Truck": {"base_rate": 16.3 * CurrentPetrolCostCanada, "fuel_efficiency": 8},  # km/l
#     "Tow Truck": {"base_rate": 25.2 * CurrentPetrolCostCanada, "fuel_efficiency": 6},  # km/l
#     "Reefers (Refrigerated Truck)": {"base_rate": 32.5 * CurrentPetrolCostCanada, "fuel_efficiency": 5},  # km/l
#     "Box Truck": {"base_rate": 39.49 * CurrentPetrolCostCanada, "fuel_efficiency": 7},  # km/l
#     "Flatbed Truck": {"base_rate": 37.4 * CurrentPetrolCostCanada, "fuel_efficiency": 6}  # km/l
# }


# # Delivery categories
# DELIVERY_CATEGORIES = {
#     "MEDICINE": 0.6,
#     "GROCERY DELIVERY": 0.9,
#     "FOOD DELIVERY": 1.0,
#     "CAR PARTS": 1.2,
#     "TORONTO LAB": 1.3,
#     "SENIOR (PACKAGE PICKUP)": 0.8,
#     "SENIOR APPOINTMENT": 1.1,
#     "CANNABIS DELIVERY": 1.2,
#     "PICKUP TRUCK": 1.0,
#     "VAN DELIVERY": 1.0,
#     "STANDARD DELIVERY": 1.0,
#     "FLOWER DELIVERY": 1.1,
#     "CAR": 1.0
# }