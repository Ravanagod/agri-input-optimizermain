def get_soil_type(state: str) -> str:
    """
    Returns dominant soil type based on Indian state.
    Fallbacks safely to 'Unknown'.
    """

    if not state:
        return "Unknown"

    state = state.strip()

    soil_by_state = {
        "Tamil Nadu": "Red Loamy Soil",
        "Andhra Pradesh": "Alluvial Soil",
        "Telangana": "Black Cotton Soil",
        "Karnataka": "Black Cotton Soil",
        "Maharashtra": "Black Cotton Soil",
        "Punjab": "Alluvial Soil",
        "Haryana": "Alluvial Soil",
        "Uttar Pradesh": "Alluvial Soil",
        "Bihar": "Alluvial Soil",
        "West Bengal": "Alluvial Soil",
        "Odisha": "Laterite Soil",
        "Chhattisgarh": "Laterite Soil",
        "Jharkhand": "Laterite Soil",
        "Kerala": "Laterite Soil",
        "Assam": "Alluvial Soil",
        "Rajasthan": "Desert / Sandy Soil",
        "Gujarat": "Black Cotton Soil",
        "Madhya Pradesh": "Black Cotton Soil",
        "Himachal Pradesh": "Mountain Soil",
        "Uttarakhand": "Mountain Soil"
    }

    return soil_by_state.get(state, "Mixed / Regional Soil")
