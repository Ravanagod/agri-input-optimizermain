def advisory_rules(ndvi):
    if ndvi is None:
        return "Satellite data unavailable. Follow standard agronomy practices."

    if ndvi < 0.3:
        return "Severe crop stress detected. Increase irrigation and inspect soil nutrients."
    elif ndvi < 0.6:
        return "Moderate crop health. Maintain irrigation and fertilizer schedule."
    else:
        return "Healthy vegetation. Yield potential is high."
