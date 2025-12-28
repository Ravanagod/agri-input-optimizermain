# optimizer/yield_model.py

def predict_yield(crop, soil, season, area, weather_df):
    """
    Weather & soil aware yield estimation
    Units: kg
    """

    base_yield = {
        "Rice": 2400,
        "Wheat": 2200,
        "Maize": 2600
    }.get(crop, 2200)

    soil_factor = {
        "Red Loamy Soil": 1.0,
        "Black Cotton Soil": 1.05,
        "Alluvial Soil": 1.05,
        "Laterite Soil": 0.9,
        "Mixed / Regional Soil": 0.95,
        "Unknown Soil": 0.95
    }.get(soil, 0.95)

    season_factor = {
        "Kharif": 1.0,
        "Rabi": 0.9,
        "Zaid": 0.8
    }.get(season, 1.0)

    avg_temp = weather_df["Temp_C"].mean()
    rain_sum = weather_df["Rain_mm"].sum()

    temp_factor = 1.0 if 20 <= avg_temp <= 35 else 0.9
    rain_factor = 1.0 if rain_sum >= 20 else 0.85

    yield_per_acre = (
        base_yield
        * soil_factor
        * season_factor
        * temp_factor
        * rain_factor
    )

    return round(yield_per_acre * area, 2)
