import requests
import json


LAT, LON = 30.5505, 79.5656

def fetch_soil_properties():
    print(f"Fetching soil texture data for Joshimath...")
    
    
    # Querying clay, sand, and silt content at the surface
    properties = ["clay", "sand", "silt"]
    depth = "0-5cm"
    
    url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lat={LAT}&lon={LON}&property=clay&property=sand&property=silt&depth={depth}&value=mean"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extracting the values 
        layers = data['properties']['layers']
        soil_profile = {}
        
        for layer in layers:
            name = layer['name']
            val = layer['depths'][0]['values']['mean'] / 10.0
            soil_profile[name] = f"{val}%"
            
        output_file = "/app/data/soil_composition.json"
        with open(output_file, 'w') as f:
            json.dump(soil_profile, f, indent=4)
            
        print("-" * 30)
        print("Soil Composition for Stochastic Input:")
        for k, v in soil_profile.items():
            print(f"{k.capitalize()}: {v}")
        print("-" * 30)
        print(f"Saved to {output_file}")
    else:
        print(f"Failed to fetch soil data. Status: {response.status_code}")

if __name__ == "__main__":
    fetch_soil_properties()