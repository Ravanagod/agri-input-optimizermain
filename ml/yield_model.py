import joblib
import os
import pandas as pd

MODEL_PATH = "ml/yield_model.pkl"

model = joblib.load(MODEL_PATH)

SOIL_MAP = {
    "Sandy": 1,
    "Loamy": 3,
    "Clay": 5
}

SEASON_MAP = {
    "Kharif": 1,
    "Rabi": 2,
    "Zaid": 3
}

def predict_yield(rainfall, temperature, soil, season, area):
    df = pd.DataFrame([{
        "rainfall_mm": rainfall,
        "temperature_c": temperature,
        "soil_code": SOIL_MAP.get(soil, 3),
        "season_code": SEASON_MAP.get(season, 1),
        "area_acres": area
    }])

    return float(model.predict(df)[0])
