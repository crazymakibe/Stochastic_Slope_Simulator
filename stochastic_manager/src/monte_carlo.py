import json
import numpy as np
import pandas as pd
from scipy.stats import qmc  # Latin Hypercube Sampling

# Paths inside the container
SOIL_DATA = "/app/data/soil_composition.json"
OUTPUT_TRIALS = "/app/data/stochastic_trials.csv"

def generate_stochastic_samples(n_samples=100):
    print("Starting Monte Carlo engine...")
    
    # Loading up the soil composition fetched earlier
    try:
        with open(SOIL_DATA, 'r') as f:
            composition = json.load(f)
    except FileNotFoundError:
        print(f"Error: {SOIL_DATA} not found. Did you run the GIS fetcher?")
        return

    # Extracting the percentages 
    clay = float(composition.get('clay', composition.get('Clay', '0%')).replace('%', ''))
    sand = float(composition.get('sand', composition.get('Sand', '0%')).replace('%', ''))

    # Pedotransfer Logic 
    phi_mean = 20.0 + (0.3 * sand)
    c_mean = 5.0 + (0.5 * clay)
    
    print(f"Mean Values Calculated: phi={phi_mean:.2f}°, c={c_mean:.2f} kPa")

    # Latin Hypercube Sampling (LHS)
    # Using d=2 for two variables
    sampler = qmc.LatinHypercube(d=2)
    sample = sampler.random(n=n_samples)
    
    # Defining bounds: [phi, cohesion]
    # Applying a +/- 10% range around the mean
    lower_bounds = [phi_mean * 0.9, c_mean * 0.9]
    upper_bounds = [phi_mean * 1.1, c_mean * 1.1]
    
    # Scaling the entire (100, 2) array correctly in one pass
    scaled_samples = qmc.scale(sample, lower_bounds, upper_bounds)

    # Saving the 100 trials to a CSV for the C++ Solver
    df = pd.DataFrame({
        'trial_id': range(n_samples),
        'phi_deg': scaled_samples[:, 0],      
        'cohesion_kpa': scaled_samples[:, 1]  
    })

    df.to_csv(OUTPUT_TRIALS, index=False)
    print(f"SUCCESS: Generated {n_samples} trials in {OUTPUT_TRIALS}")

if __name__ == "__main__":
    generate_stochastic_samples()