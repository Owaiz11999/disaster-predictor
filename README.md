# 🌍 AI-Powered Disaster Impact Predictor & Emergency Resource Recommender

Streamlit web app to predict disaster severity and recommend emergency resources.

## Features
- ✅ **ML-Based Severity Prediction**  
  Uses a trained Random Forest model to estimate the impact level of a disaster based on parameters like type, magnitude, and casualties.

- ✅ **Automated Emergency Resource Planning**  
  Recommends critical resources (water, food, tents, medical units, rescue teams) dynamically based on severity and population affected.

- ✅ **Interactive Geospatial Map**  
  Visualizes historical disaster data across regions using `Folium` and `GeoPandas` for deeper insights into vulnerable areas.

- ✅ **Top 10 Disaster-Prone Regions**  
  Automatically computes and displays the countries with the highest disaster frequency.



## 🛠️ Tech Stack

- **Frontend:** Streamlit, Folium (via `streamlit-folium`)
- **Backend:** Python (Pandas, Scikit-learn, Joblib)
- **ML Model:** Random Forest Regressor (via `Pipeline` and `ColumnTransformer`)
- **Geospatial:** GeoPandas, Shapely
- **Data Source:** EM-DAT International Disaster Database



├── main.py                  # Streamlit app
├── utils/
│   ├── train.py             # Model training & prediction
│   ├── geograph.py          # Geospatial utilities
│   └── resource.py          # Emergency resource recommendation logic
├── models/
│   └── impact_predictor.pkl # Trained Random Forest model
├── data/
│   └── emdat_disasters.xlsx # Source data
└── requirements.txt


## Setup
```bash
git clone https://github.com/Owaiz11999/disaster-predictor.git
cd disaster-predictor
pip install -r requirements.txt
streamlit run main.py
```
