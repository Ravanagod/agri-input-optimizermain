import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_ndvi(lat, lon, days=30):
    try:
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

        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()

        ndvi = data.get("properties", {}).get("parameter", {}).get("NDVI", {})
        if not ndvi:
            return None

        df = pd.DataFrame({
            "date": pd.to_datetime(ndvi.keys()),
            "ndvi": list(ndvi.values())
        }).dropna()

        return df if not df.empty else None

    except Exception:
        return None


def ndvi_health(avg):
    if avg >= 0.6:
        return "Healthy Crop", "green"
    elif avg >= 0.3:
        return "Moderate Vegetation", "orange"
    else:
        return "Crop Stress", "red"
