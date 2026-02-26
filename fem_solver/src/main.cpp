#include <iostream>
#include <vector>
#include <gdal_priv.h>
#include "slope_stability.h"

int main() {
    std::cout << "--- Joshimath FEM Solver: Real Data Integration ---" << std::endl;

    GDALAllRegister();
    // Points to the shared volume
    const char* pszFilename = "/app/shared_data/joshimath_terrain.tif";
    GDALDataset *poDataset = (GDALDataset *) GDALOpen(pszFilename, GA_ReadOnly);

    if (poDataset == NULL) {
        std::cerr << "CRITICAL ERROR: Could not find /app/shared_data/joshimath_terrain.tif!" << std::endl;
        return 1;
    }

    GDALRasterBand *poBand = poDataset->GetRasterBand(1);
    int width = poBand->GetXSize();

    std::vector<double> real_elevations(width);
    poBand->RasterIO(GF_Read, 0, 0, width, 1, &real_elevations[0], width, 1, GDT_Float64, 0, 0);

    std::cout << "Successfully ingested " << width << " terrain nodes." << std::endl;

    SlopeStabilitySolver solver(real_elevations);
    solver.run();

    GDALClose(poDataset);
    return 0;
}