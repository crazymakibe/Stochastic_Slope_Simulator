import requests
import json
import os
from datetime import datetime

# Coordinates for Joshimath 
LAT = 30.5505
LON = 79.5656


OUTPUT_PATH = "/app/data/live_data.json"

def fetch_joshimath_weather():
    """
    Fetches live rainfall data and saves it for the Stochastic Manager.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Connecting to Open-Meteo API...")
    
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}&"
        f"current_weather=true&"
        f"daily=precipitation_sum&"
        f"timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Checking for HTTP errors
        
        data = response.json()
        
        # Extracting the key variables for the FEM solver
        current_temp = data['current_weather']['temperature']
        rainfall_z = data['daily']['precipitation_sum'][0]
        timestamp = datetime.now().isoformat()

        weather_payload = {
            "metadata": {
                "location": "Joshimath, Uttarakhand",
                "coordinates": {"lat": LAT, "lon": LON},
                "last_updated": timestamp
            },
            "parameters": {
                "rainfall_mm_z": rainfall_z,
                "temp_c": current_temp
            }
        }

        # Ensuring the directory exists and writing the JSON
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w") as f:
            json.dump(weather_payload, f, indent=4)

        print("-" * 40)
        print(f"SUCCESS: Live Rainfall (z) = {rainfall_z} mm")
        print(f"Data saved to shared volume: {OUTPUT_PATH}")
        print("-" * 40)

    except requests.exceptions.RequestException as e:
        print(f"CRITICAL ERROR: Could not fetch weather data. {e}")
        

if __name__ == "__main__":
    fetch_joshimath_weather()
