from geopy.geocoders import Nominatim

_geolocator = Nominatim(user_agent="ai-agri-optimizer")


def get_coordinates(place: str):
    """
    Returns (lat, lon) for a place / city / PIN.
    """
    try:
        location = _geolocator.geocode(place, timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass

    return None, None


def get_location_name(lat: float, lon: float):
    """
    Reverse geocoding:
    Returns a readable location name from coordinates.
    """
    try:
        location = _geolocator.reverse((lat, lon), timeout=10)
        if location:
            return location.address
    except Exception:
        pass

    return "Location not available"
