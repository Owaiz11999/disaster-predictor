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
st.title("AI-Powered Disaster Impact Predictor & Emergency Resource Recommender")

st.sidebar.header("Enter Disaster Parameters")

disaster_type = st.sidebar.selectbox("Disaster Type", ["Earthquake", "Flood", "Cyclone", "Drought"])
magnitude = st.sidebar.slider("Magnitude / Severity Level", 1.0, 10.0, 5.5)
total_affected = st.sidebar.number_input("Estimated Affected Population", 100, 1000000, 1000)
total_deaths = st.sidebar.number_input("Estimated Deaths", 0, 100000, 50)

if st.sidebar.button("Predict & Recommend"):
    input_data = [disaster_type, magnitude, total_affected, total_deaths]
    severity_score = predict_impact(input_data)
    st.success(f"Predicted Damage Severity Score: {severity_score:,.2f}")

    resources = recommend_resources(severity_score, population_affected=total_affected)
    st.subheader("Recommended Emergency Resources")
    st.write(resources)

st.subheader("Historical Disaster Map (EM-DAT)")
try:
    df = pd.read_excel('data/emdat_data.xlsx')
    df['Year'] = pd.to_datetime(df['Start Year'], errors='coerce').dt.year
    gdf = prepare_disaster_geodf(df, lon_col='Longitude', lat_col='Latitude')
    world = load_region_geojson('https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson')
    fmap = plot_disasters_on_map(gdf, region_gdf=world)
    st_folium(fmap, width=900, height=500)
except Exception as e:
    st.error("Error loading map or dataset.")
    st.exception(e)

if st.checkbox("Show Top 10 Disaster-Prone Countries"):
    try:
        counts = count_disasters_by_region(gdf, world, region_key='ADMIN')
        top_counts = counts.sort_values('disaster_count', ascending=False).head(10)
        st.dataframe(top_counts)
    except:
        st.warning("Unable to compute disaster counts.")
