python3 -m venv venv
. venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
.env:
GOOGLE_MAPS_API_KEY
uvicorn main:app --reload

#testData:
{
  "pickup_address": "Toronto, ON",
  "delivery_address": "Mississauga, ON",
  "delivery_category": "MEDICINE",
  "vehicle_type": "Car"
}

{
  "pickup_address": "Vancouver, BC",
  "delivery_address": "Surrey, BC",
  "delivery_category": "GROCERY DELIVERY",
  "vehicle_type": "Van"
}
{
  "pickup_address": "Ottawa, ON",
  "delivery_address": "Montreal, QC",
  "delivery_category": "STANDARD DELIVERY",
  "vehicle_type": "Pickup Truck"
}
{
  "pickup_address": "Calgary, AB",
  "delivery_address": "Edmonton, AB",
  "delivery_category": "CANNABIS DELIVERY",
  "vehicle_type": "Flatbed Truck"
}
{
  "pickup_address": "New York, NY",
  "delivery_address": "Brooklyn, NY",
  "delivery_category": "FOOD DELIVERY",
  "vehicle_type": "Bicycle"
}



