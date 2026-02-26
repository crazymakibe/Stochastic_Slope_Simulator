import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os

st.set_page_config(page_title="Joshimath Slope Stability Monitor", layout="wide")


# Checking for data in Docker mount, GitHub root, or local folder
possible_paths = [
    "shared_data/results.csv",        
    "/app/shared_data/results.csv",   
    "results.csv"                     
]

data_path = None
for path in possible_paths:
    if os.path.exists(path):
        data_path = path
        break

st.title("Joshimath Slope Stability: Stochastic Analysis")
st.markdown("This dashboard visualizes the probability of slope failure based on real-world terrain and stochastic soil parameters.")


if data_path:
    try:
        df = pd.read_csv(data_path)
        
        # Core Calculation: Probability of Failure (Pf)
        failures = df[df['FoS'] < 1.0].shape[0]
        pf = (failures / len(df)) * 100

        
        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Monte Carlo Trials", len(df))
        m2.metric("Unstable Scenarios (FoS < 1)", failures)
        m3.metric("Probability of Failure", f"{pf:.1f}%", 
                  delta=" HIGH RISK" if pf > 15 else " STABLE", 
                  delta_color="inverse")
        st.markdown("---")

        
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader(" Distribution of Safety Factors")
            # Factor of Safety Histogram
            fig_hist = ff.create_distplot([df['FoS'].dropna()], ['Factor of Safety'], 
                                          bin_size=0.05, show_rug=False, colors=['#00CC96'])
            # Failure Threshold Line
            fig_hist.add_vline(x=1.0, line_dash="dash", line_color="#EF553B", 
                               annotation_text="FAILURE LIMIT")
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_right:
            st.subheader(" Parameter Sensitivity")
            # Scatter showing how Cohesion and Friction interact to affect FoS
            fig_scatter = px.scatter(df, x="Cohesion", y="Friction", color="FoS", 
                                     size="Rainfall", hover_data=['Trial_ID'],
                                     color_continuous_scale='RdYlGn',
                                     labels={'FoS': 'Safety Factor'})
            st.plotly_chart(fig_scatter, use_container_width=True)


        with st.expander("View Raw Simulation Data"):
            st.dataframe(df.sort_values(by="FoS"), use_container_width=True)

    except Exception as e:
        st.error(f"Error loading results.csv: {e}")
else:
    st.warning("**Data Sync Required:** Run the C++ Solver on your local machine to generate `results.csv`, then push it to GitHub to update this dashboard.")