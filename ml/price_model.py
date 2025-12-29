def predict_price(crop):
    prices = {
        "Rice": 25,
        "Wheat": 22,
        "Maize": 20
    }
    return prices.get(crop, 20)
