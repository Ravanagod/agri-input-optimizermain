def generate_alerts(ndvi):
    if ndvi is None:
        return ["Satellite data unavailable"]

    if ndvi < 0.4:
        return ["⚠ Crop stress risk detected"]
    return ["✅ Crop health is stable"]
