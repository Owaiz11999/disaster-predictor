import streamlit as st
import pandas as pd
from utils.train import predict_impact 
from utils.resource import recommend_resources
from utils.geograph import (
    load_region_geojson, prepare_disaster_geodf,
    plot_disasters_on_map, count_disasters_by_region
)

from streamlit_folium import st_folium

st.set_page_config(page_title="Disaster Predictor & Resource Planner", layout="wide")
st.title(" AI-Powered Disaster Impact Predictor & Emergency Resource Recommender")
st.markdown("---")

st.sidebar.header(" Enter Disaster Parameters")

disaster_type = st.sidebar.selectbox("Disaster Type", ["Earthquake", "Flood", "Cyclone", "Drought"])
magnitude = st.sidebar.slider("Magnitude / Severity Level", 1.0, 10.0, 5.5)
total_affected = st.sidebar.number_input("Estimated Affected Population", 100, 1_000_000, 1000, step=100)
total_deaths = st.sidebar.number_input("Estimated Deaths", 0, 100_000, 50, step=10)

col1, col2 = st.columns(2)
if st.sidebar.button(" Predict & Recommend"):
    with st.spinner("Running prediction and preparing recommendations..."):
        input_data = [disaster_type, magnitude, total_affected, total_deaths]
        severity_score = predict_impact(input_data)

        col1.metric("Predicted Damage Severity Score", f"{severity_score:.2f}", delta=None)
        
        resources = recommend_resources(severity_score, population_affected=total_affected)
        col2.subheader(" Recommended Emergency Resources")
        with st.expander("View Recommended Supplies"):
            st.table(resources)

        
        csv = pd.DataFrame(resources.items(), columns=["Resource", "Quantity"]).to_csv(index=False).encode('utf-8')
        st.download_button(" Download Recommendations (CSV)", data=csv, file_name='emergency_resources.csv', mime='text/csv')

st.markdown("##  Historical Disaster Map (EM-DAT)")
try:
    df = pd.read_excel('/Users/owaisjamadar/Downloads/public_emdat_custom_request_2025-06-21_213dd491-fb17-4c63-84af-8e8df02faed8.xlsx')
    df['Year'] = pd.to_numeric(df['Start Year'], errors='coerce')
    df = df[df['Year'].notna()]
    df['Year'] = df['Year'].astype(int)
    gdf = prepare_disaster_geodf(df, lon_col='Longitude', lat_col='Latitude')
    world = load_region_geojson('https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson')
    fmap = plot_disasters_on_map(gdf, region_gdf=world)
    st_folium(fmap, width=1000, height=500)
except Exception as e:
    st.error(" Error loading map or dataset.")
    st.exception(e)

st.markdown("## Top 10 Disaster-Prone Countries")
if st.checkbox("Show Top 10 Countries"):
    try:
        counts = count_disasters_by_region(gdf, world, region_key='ADMIN')
        top_counts = counts.sort_values('disaster_count', ascending=False).head(10)
        st.dataframe(top_counts.reset_index(drop=True))
    except Exception as e:
        st.warning(" Could not calculate disaster statistics.")
        st.exception(e)
