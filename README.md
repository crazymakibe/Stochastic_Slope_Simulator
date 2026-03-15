# Joshimath Slope Stability: Stochastic FEM Analysis System

This project provides a professional-grade simulation environment for assessing landslide risks in Joshimath, Uttarakhand. It bridges high-performance C++ Finite Element Method (FEM) analysis with real-world geospatial data and a live risk-monitoring dashboard.

---

## 1. Physical and Mathematical Framework

The core of the simulation is based on the limit equilibrium of soil masses, modeled through the Mohr-Coulomb failure criterion.

### Shear Strength and Effective Stress
The shear strength of the soil ($\tau$) is calculated using the effective stress principle to account for pore water pressure ($u$):

$$\tau = c + (\sigma - u) \tan(\phi)$$

Where:
* $c$: Soil Cohesion (Pa)
* $\sigma$: Total Normal Stress (Pa)
* $u$: Pore Water Pressure (Pa), derived from live rainfall data: $u = \rho_w \cdot g \cdot h_{rain}$
* $\phi$: Internal Angle of Friction (degrees)

### Factor of Safety (FoS) Assembly
The global stability is determined by the ratio of resisting forces ($S_r$) to driving forces ($S_d$). In our FEM mesh, we integrate these forces over each active cell:

$$FoS = \frac{\sum_{i=1}^{n} [c \cdot L_i + (W_i \cos \alpha_i - u_i \cdot L_i) \tan \phi]}{\sum_{i=1}^{n} W_i \sin \alpha_i}$$

Where:
* $W_i$: Weight of the soil element ($Area \times Density \times g$)
* $\alpha_i$: Local slope angle calculated from GDAL elevation nodes
* $L_i$: Length of the failure plane segment

### Stochastic Monte Carlo Method
To account for soil heterogeneity, we do not treat $c$ and $\phi$ as constants. We perform $N$ trials where:
$$c_{trial} \sim \mathcal{N}(\mu_c, \sigma_c^2)$$
$$\phi_{trial} \sim \mathcal{N}(\mu_\phi, \sigma_\phi^2)$$

This allows the calculation of the **Probability of Failure ($P_f$)**:
$$P_f = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(FoS_j < 1.0)$$

---

## 2. Technical Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Data Ingestion** | GDAL / Python | GeoTIFF (DEM) processing and node extraction |
| **Simulation Core** | C++17 / deal.II | Finite Element Assembly and Stochastic Solver |
| **Data Context** | JSON | Live Rainfall and Soil Composition integration |
| **Visualization** | Python / Streamlit | Real-time Risk Dashboard and Plotly analytics |
| **Orchestration** | Docker | Containerized microservices for portability |

---

## 3. Project Structure

├── gis_fetcher/           # GDAL-based terrain extraction

├── fem_solver/            # C++/deal.II Source Code

├── dashboard/             # Streamlit UI (app.py)

├── shared_data/           # GeoTIFFs, live_data.json, results.csv

├── docker-compose.yml     # Multi-container orchestration

└── .gitignore             # Security and hygiene rules

---

## 4. Forking and Local Setup

### Prerequisites
* Docker Engine and Docker Compose
* CMake (for local C++ builds)

### Installation
1. Clone the repository:
   git clone https://github.com/crazymakibe/joshimath-stochastic-stability.git
   cd joshimath-stochastic-stability

2. Generate the Terrain Data:
   Ensure your .env is set in gis_fetcher/, then run the fetcher to generate the GeoTIFF.

3. Run the FEM Solver:
   cd fem_solver/build
   cmake ..
   make
   ./joshimath_solver

4. Launch the Dashboard:
   docker run -d -p 8501:8501 -v $(pwd)/shared_data:/app/shared_data --name risk_ui risk_dashboard

---

## 5. Deployment Note
This dashboard is configured for Hybrid Hosting. The heavy FEM calculations are performed on the local "Edge" machine (PC), while the results.csv is pushed to GitHub to update the public Streamlit Cloud dashboard.
