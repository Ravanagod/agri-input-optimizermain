from ml.yield_model import predict_yield_ml
from ml.price_model import predict_price

def predict_all(crop, soil, season, weather_df, area):
    avg_rain = weather_df["Rain_mm"].mean()
    avg_temp = weather_df["Temp_C"].mean()

    yield_kg = predict_yield_ml(
        crop=crop,
        soil=soil,
        season=season,
        rain=avg_rain,
        temp=avg_temp,
        area=area
    )

    price = predict_price(crop)
    revenue = yield_kg * price

    return {
        "yield": round(yield_kg, 2),
        "price": price,
        "revenue": round(revenue, 2)
    }
