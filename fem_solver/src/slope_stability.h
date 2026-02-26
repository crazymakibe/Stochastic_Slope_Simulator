#ifndef SLOPE_STABILITY_H
#define SLOPE_STABILITY_H

#include <deal.II/grid/tria.h>
#include <deal.II/dofs/dof_handler.h>
#include <deal.II/fe/fe_q.h>
#include <deal.II/lac/vector.h>
#include <deal.II/lac/sparse_matrix.h>
#include <deal.II/lac/dynamic_sparsity_pattern.h>
#include <vector>
#include <string>

using namespace dealii;

class SlopeStabilitySolver {
public:
    SlopeStabilitySolver(const std::vector<double> &elevations);
    void run();

private:
    void make_grid();
    void setup_system();
    // Added the 4th argument: density
    double calculate_fos(double cohesion, double phi, double rain, double density);

    Triangulation<2> triangulation;
    FE_Q<2>          fe;
    DoFHandler<2>    dof_handler;

    SparsityPattern      sparsity_pattern;
    SparseMatrix<double> system_matrix;
    Vector<double>       solution;
    Vector<double>       system_rhs;

    std::vector<double> elevation_data;
};

#endif