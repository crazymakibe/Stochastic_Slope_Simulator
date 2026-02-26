import rasterio
import numpy as np

FILE_PATH = "/app/data/joshimath_terrain.tif"

def verify_data():
    try:
        with rasterio.open(FILE_PATH) as dataset:
            print(f"--- Terrain Inspection: {FILE_PATH} ---")
            print(f"Width:  {dataset.width} pixels")
            print(f"Height: {dataset.height} pixels")
            print(f"Bands:  {dataset.count}")
            print(f"CRS:    {dataset.crs}") 
            

            elevation = dataset.read(1)
            
            min_elev = np.min(elevation)
            max_elev = np.max(elevation)
            mean_elev = np.mean(elevation)

            print(f"Min Elevation:  {min_elev:.2f} m")
            print(f"Max Elevation:  {max_elev:.2f} m")
            print(f"Mean Elevation: {mean_elev:.2f} m")
            print("-" * 30)

            if min_elev < 0:
                print("Warning: Found negative elevations. Check if data is valid.")
            else:
                print("Verification Complete: Terrain data looks healthy.")

    except Exception as e:
        print(f"Verification Failed: {e}")

if __name__ == "__main__":
    verify_data()