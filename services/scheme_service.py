def get_schemes_by_state(state: str):
    """
    Returns list of government schemes relevant to the farmer's state.
    Includes central + state-specific schemes.
    """

    central_schemes = [
        "PM-KISAN – ₹6000/year income support",
        "PMFBY – Crop insurance scheme",
        "Soil Health Card Scheme",
        "Kisan Credit Card (KCC)",
        "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)"
    ]

    state_schemes = {
        "Tamil Nadu": [
            "Kuruvai Special Package",
            "Free Electricity for Farmers",
            "Chief Minister’s Farmers Protection Scheme"
        ],
        "Andhra Pradesh": [
            "YSR Rythu Bharosa",
            "Free Borewell Scheme",
            "Crop Input Subsidy Scheme"
        ],
        "Telangana": [
            "Rythu Bandhu",
            "Rythu Bima (Farmer Insurance)"
        ],
        "Karnataka": [
            "Raitha Siri",
            "Krushi Bhagya Yojana"
        ],
        "Maharashtra": [
            "Mahadbt Farmer Subsidy Scheme",
            "Baliraja Electricity Subsidy"
        ],
        "Punjab": [
            "Punjab Smart Seeder Subsidy",
            "Free Power for Agriculture"
        ],
        "Kerala": [
            "Subhiksha Keralam",
            "Karshaka Pension Scheme"
        ]
    }

    if not state:
        return central_schemes

    return central_schemes + state_schemes.get(state, [])
