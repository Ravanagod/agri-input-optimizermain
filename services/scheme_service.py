def get_schemes(state_or_place: str, crop: str | None = None):
    """
    Return government schemes based on Indian state.
    Works even if full place name is given.
    """

    text = state_or_place.lower()

    schemes_by_state = {
        "tamil nadu": [
            "Kuruvai Special Package – Subsidy for short-term crops",
            "Tamil Nadu Farmers Crop Insurance Scheme (TNFCIS)",
            "Free electricity for agriculture pumpsets",
            "Soil Health Card Scheme",
            "PM-KISAN – ₹6000/year income support"
        ],

        "andhra pradesh": [
            "YSR Rythu Bharosa – ₹13,500/year financial support",
            "Andhra Pradesh Crop Insurance Scheme",
            "Free borewell scheme for small farmers",
            "Soil Health Card Scheme",
            "PM-KISAN – ₹6000/year income support"
        ],

        "karnataka": [
            "Raitha Siri – Direct income support",
            "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "Karnataka Krushi Yantra Dhare – Machinery subsidy",
            "Soil Health Card Scheme",
            "PM-KISAN – ₹6000/year income support"
        ],

        "telangana": [
            "Rythu Bandhu – Investment support per acre",
            "Rythu Bima – Farmer life insurance",
            "Mission Kakatiya – Irrigation tanks restoration",
            "Soil Health Card Scheme",
            "PM-KISAN – ₹6000/year income support"
        ],

        "maharashtra": [
            "MahaDBT Farmer Schemes",
            "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "Farm pond subsidy scheme",
            "Soil Health Card Scheme",
            "PM-KISAN – ₹6000/year income support"
        ]
    }

    # Detect state from place string
    for state, schemes in schemes_by_state.items():
        if state in text:
            return schemes

    # Fallback (India-wide schemes)
    return [
        "PM-KISAN – ₹6000/year income support",
        "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "Soil Health Card Scheme",
        "Kisan Credit Card (KCC)"
    ]
