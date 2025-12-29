import joblib
import numpy as np

model = joblib.load("ml/yield_model.pkl")

def predict_yield_ml(crop, soil, season, rain, temp, area):
    crop_map = {"Rice": 0, "Wheat": 1, "Maize": 2}
    soil_map = {"Red Loamy Soil": 0, "Black Cotton Soil": 1}
    season_map = {"Kharif": 0, "Rabi": 1}

    X = np.array([[
        crop_map.get(crop, 0),
        soil_map.get(soil, 0),
        season_map.get(season, 0),
        rain,
        temp
    ]])

    yield_per_acre = model.predict(X)[0]
    return yield_per_acre * area
