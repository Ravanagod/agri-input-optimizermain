# services/soil_service.py

"""
Soil classification service
Rule-based soil mapping by Indian states
Stable & offline (no API → no crashes)
"""

STATE_SOIL_MAP = {
    "Tamil Nadu": "Red Loamy Soil",
    "Andhra Pradesh": "Black Cotton Soil",
    "Telangana": "Black Soil",
    "Karnataka": "Red Soil",
    "Kerala": "Laterite Soil",
    "Maharashtra": "Black Cotton Soil",
    "Punjab": "Alluvial Soil",
    "Haryana": "Alluvial Soil",
    "Uttar Pradesh": "Alluvial Soil",
    "Rajasthan": "Desert Sandy Soil",
    "Madhya Pradesh": "Black Soil",
    "Bihar": "Alluvial Soil",
    "West Bengal": "Alluvial Soil",
    "Odisha": "Red & Laterite Soil",
}

def get_soil_type(state: str) -> str:
    """
    Returns dominant soil type for a given Indian state
    """

    if not state:
        return "Unknown Soil"

    return STATE_SOIL_MAP.get(state.strip(), "Mixed / Regional Soil")
