# services/weather_service.py

import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_weather(lat, lon, days=5):
    """
    Fetch last N days weather from NASA POWER
    Returns DataFrame with Temp_C and Rain_mm
    Always safe (no KeyError)
    """

    end = datetime.utcnow().date()
    start = end - timedelta(days=days)

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        "?parameters=T2M,PRECTOTCORR"
        f"&latitude={lat}&longitude={lon}"
        f"&start={start.strftime('%Y%m%d')}"
        f"&end={end.strftime('%Y%m%d')}"
        "&community=AG&format=JSON"
    )

    r = requests.get(url, timeout=15)
    r.raise_for_status()

    js = r.json()
    params = js.get("properties", {}).get("parameter", {})

    temp = params.get("T2M", {})
    rain = params.get("PRECTOTCORR", {})

    # Build dataframe safely
    df = pd.DataFrame({
        "Date": pd.to_datetime(list(temp.keys())),
        "Temp_C": list(temp.values()),
        "Rain_mm": [rain.get(d, 0) for d in temp.keys()]
    })

    df = df.dropna().sort_values("Date")

    return df
