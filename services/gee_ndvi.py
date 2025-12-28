import ee
import pandas as pd
from datetime import datetime, timedelta

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize()


def get_ndvi_timeseries(lat, lon, days=30):
    """
    Get NDVI time series from MODIS (works everywhere)
    """

    point = ee.Geometry.Point([lon, lat])

    end = ee.Date(datetime.utcnow().strftime("%Y-%m-%d"))
    start = end.advance(-days, "day")

    collection = (
        ee.ImageCollection("MODIS/006/MOD13Q1")
        .filterBounds(point)
        .filterDate(start, end)
        .select("NDVI")
    )

    def extract(image):
        val = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=250
        ).get("NDVI")

        return ee.Feature(None, {
            "date": image.date().format("YYYY-MM-dd"),
            "ndvi": ee.Number(val).multiply(0.0001)
        })

    features = collection.map(extract).getInfo()["features"]

    data = [
        {
            "date": f["properties"]["date"],
            "ndvi": f["properties"]["ndvi"]
        }
        for f in features
        if f["properties"]["ndvi"] is not None
    ]

    return pd.DataFrame(data)
