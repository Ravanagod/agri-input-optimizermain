def predict_yield(crop, soil, season, area, weather_df=None):
    base_yield = {
        "Rice": 2400,
        "Wheat": 2200,
        "Maize": 2600
    }.get(crop, 2200)

    soil_factor = {
        "Alluvial Soil": 1.1,
        "Black Cotton Soil": 1.15,
        "Red Loamy Soil": 1.0,
        "Laterite Soil": 0.9,
        "Unknown": 0.95
    }.get(soil, 0.95)

    season_factor = {
        "Kharif": 1.0,
        "Rabi": 0.9,
        "Zaid": 0.85
    }.get(season, 1.0)

    weather_factor = 1.0
    if weather_df is not None and not weather_df.empty:
        avg_rain = weather_df["Rain_mm"].mean()
        if avg_rain < 2:
            weather_factor = 0.9
        elif avg_rain > 6:
            weather_factor = 1.05

    yield_kg = base_yield * soil_factor * season_factor * weather_factor * area
    return round(yield_kg, 2)
