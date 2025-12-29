from geopy.geocoders import Nominatim

_geolocator = Nominatim(user_agent="ai_agri_app", timeout=10)

def get_coordinates(place: str):
    location = _geolocator.geocode(place + ", India")
    if not location:
        raise ValueError("Location not found")
    return location.latitude, location.longitude, location.address

def get_state_from_address(address: str):
    for part in address.split(","):
        if part.strip() in [
            "Tamil Nadu", "Andhra Pradesh", "Telangana", "Karnataka",
            "Maharashtra", "Kerala", "Punjab", "Haryana", "Uttar Pradesh"
        ]:
            return part.strip()
    return "Unknown"
