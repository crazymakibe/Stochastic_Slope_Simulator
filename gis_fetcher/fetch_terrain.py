import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENTOPO_API_KEY")

# Joshimath Bounding Box
BOUNDS = {
    "south": 30.540,
    "north": 30.560,
    "west": 79.550,
    "east": 79.570
}

def fetch_dem():
   
    url = "https://portal.opentopography.org/API/globaldem"
    
    params = {
        "demtype": "AW3D30",  
        "south": BOUNDS["south"],
        "north": BOUNDS["north"],
        "west": BOUNDS["west"],
        "east": BOUNDS["east"],
        "outputFormat": "GTiff",
        "API_Key": API_KEY
    }
    
    print(f"Requesting data from: {url}")
    
    try:
        
        response = requests.get(url, params=params, stream=True, timeout=30)
        
        if response.status_code == 200:
            output_file = "/app/data/joshimath_terrain.tif"
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"SUCCESS: Terrain saved to {output_file}")
        else:
            print(f"API Error ({response.status_code}):")
            print(response.text)

    except Exception as e:
        print(f"Network error occurred: {e}")

if __name__ == "__main__":
    fetch_dem()