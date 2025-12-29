import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_ndvi_nasa(lat, lon, days=30):
    end = datetime.utcnow().date()
    start = end - timedelta(days=days)

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        "?parameters=NDVI"
        f"&latitude={lat}&longitude={lon}"
        f"&start={start.strftime('%Y%m%d')}"
        f"&end={end.strftime('%Y%m%d')}"
        "&community=AG&format=JSON"
    )

    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()

    nd = data.get("properties", {}).get("parameter", {}).get("NDVI", {})
    if not nd:
        return None

    df = pd.DataFrame({
        "Date": pd.to_datetime(nd.keys()),
        "NDVI": nd.values()
    }).dropna()

    return df.sort_values("Date")

def ndvi_status(avg):
    if avg >= 0.6:
        return "Healthy Crop", "green"
    if avg >= 0.3:
        return "Moderate Vegetation", "orange"
    return "Crop Stress", "red"
