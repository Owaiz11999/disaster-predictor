import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

def train_model(data_path='data/emdat_data.xlsx', model_path='models/impact_predictor.pkl'):
    df = pd.read_excel(data_path)
    df.columns = df.columns.str.strip()
    recon_col = next((col for col in df.columns if "Reconstruction Costs" in col and "Adjusted" in col), None)
    if not recon_col:
        raise ValueError("Reconstruction cost column not found in dataset.")
    df = df[['Disaster Type', 'Magnitude', 'Total Affected', 'Total Deaths', recon_col]].dropna()
    X = df[['Disaster Type', 'Magnitude', 'Total Affected', 'Total Deaths']]
    y = df[recon_col]
    categorical_features = ['Disaster Type']
    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ], remainder='passthrough')
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    model.fit(X, y)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    return model

def predict_impact(input_data, model_path='models/impact_predictor.pkl'):
    model = joblib.load(model_path)
    columns = ['Disaster Type', 'Magnitude', 'Total Affected', 'Total Deaths']
    input_df = pd.DataFrame([input_data], columns=columns)
    return model.predict(input_df)[0]
