import pandas as pd
from datetime import datetime, timedelta

def fetch_weather(lat, lon):
    dates = [datetime.now().date() - timedelta(days=i) for i in range(5)]

    return pd.DataFrame({
        "Date": dates,
        "Temp_C": [28, 29, 30, 31, 30],
        "Rain_mm": [1, 0, 4, 2, 0]
    })
