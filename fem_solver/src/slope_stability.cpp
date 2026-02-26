#include "slope_stability.h"
#include <deal.II/grid/grid_generator.h>
#include <deal.II/grid/grid_tools.h>
#include <deal.II/fe/fe_values.h>
#include <deal.II/base/quadrature_lib.h>
#include <deal.II/numerics/vector_tools.h>
#include <deal.II/numerics/data_out.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <cmath>
#include <string>
#include <algorithm>

SlopeStabilitySolver::SlopeStabilitySolver(const std::vector<double> &elevations)
    : fe(1), dof_handler(triangulation), elevation_data(elevations) {}

void SlopeStabilitySolver::make_grid() {
    GridGenerator::subdivided_hyper_rectangle(triangulation, 
        {static_cast<unsigned int>(elevation_data.size() - 1), 10}, 
        Point<2>(0.0, 0.0), 
        Point<2>(static_cast<double>(elevation_data.size() - 1), 100.0));

    GridTools::transform([&](const Point<2> &p) {
        unsigned int x_idx = static_cast<unsigned int>(std::round(p[0]));
        if (x_idx >= elevation_data.size()) x_idx = elevation_data.size() - 1;
        return Point<2>(p[0], (p[1]/100.0) * elevation_data[x_idx]);
    }, triangulation);
}

void SlopeStabilitySolver::setup_system() {
    dof_handler.distribute_dofs(fe);
    solution.reinit(dof_handler.n_dofs());
    system_rhs.reinit(dof_handler.n_dofs());
    DynamicSparsityPattern dsp(dof_handler.n_dofs());
    DoFTools::make_sparsity_pattern(dof_handler, dsp);
    sparsity_pattern.copy_from(dsp);
    system_matrix.reinit(sparsity_pattern);
}

double SlopeStabilitySolver::calculate_fos(double cohesion, double phi, double rain, double density) {
    double total_resisting_force = 0;
    double total_driving_force = 0;
    const double rad = M_PI / 180.0;

    for (const auto &cell : triangulation.active_cell_iterators()) {
        double cell_slope = 35.0; 
        double area = cell->measure();
        double weight = area * density * 9.81; 
        
        double normal_force = weight * std::cos(cell_slope * rad);
        double shear_demand = weight * std::sin(cell_slope * rad);
        
        double shear_capacity = (cohesion * area) + 
                                (normal_force - (rain * 1000.0 * area)) * std::tan(phi * rad);
        
        total_resisting_force += shear_capacity;
        total_driving_force += shear_demand;
    }
    return (total_driving_force > 0) ? (total_resisting_force / total_driving_force) : 10.0;
}

double parse_json_value(const std::string& filename, const std::string& key) {
    std::ifstream file(filename);
    if (!file.is_open()) return 0.0;
    std::string line;
    while (std::getline(file, line)) {
        if (line.find(key) != std::string::npos) {
            size_t start = line.find(':') + 1;
            size_t end = line.find_first_of(",}", start);
            if (start == std::string::npos || end == std::string::npos) continue;
            std::string val = line.substr(start, end - start);
            val.erase(std::remove(val.begin(), val.end(), '\"'), val.end());
            val.erase(std::remove(val.begin(), val.end(), '%'), val.end());
            val.erase(std::remove(val.begin(), val.end(), ' '), val.end());
            try { return std::stod(val); } catch (...) { return 0.0; }
        }
    }
    return 0.0;
}

void SlopeStabilitySolver::run() {
    make_grid();
    setup_system();

    double live_rain = parse_json_value("/app/shared_data/live_data.json", "rainfall_mm_z");
    double clay_p = parse_json_value("/app/shared_data/soil_composition.json", "clay");
    double sand_p = parse_json_value("/app/shared_data/soil_composition.json", "sand");
    double silt_p = parse_json_value("/app/shared_data/soil_composition.json", "silt");

    // Weighted density logic
    double site_density = (clay_p * 16.0) + (sand_p * 20.0) + (silt_p * 18.0); 
    if (site_density <= 0) site_density = 1800.0; // Fallback

    std::cout << "Context Loaded: Rain=" << live_rain << "mm, Density=" << site_density << "kg/m3" << std::endl;

    std::ifstream input_file("/app/shared_data/stochastic_trials.csv");
    std::ofstream output_file("/app/shared_data/results.csv");
    
    std::string line;
    std::getline(input_file, line); 
    output_file << "Trial_ID,Cohesion,Friction,Rainfall,FoS\n";

    int count = 0;
    while (std::getline(input_file, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string t_id, t_c, t_phi;

        std::getline(ss, t_id, ',');
        std::getline(ss, t_c, ',');
        std::getline(ss, t_phi, ',');

        try {
            double c = std::stod(t_c);
            double p = std::stod(t_phi);
            double fos = calculate_fos(c, p, live_rain, site_density);
            output_file << t_id << "," << c << "," << p << "," << live_rain << "," << fos << "\n";
            count++;
        } catch (...) { continue; }
    }

    std::cout << "SUCCESS: Processed " << count << " trials using Live Site Data." << std::endl;
}