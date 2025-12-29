def optimize_cost(area, crop):
    base_cost = {
        "Rice": 18000,
        "Wheat": 15000,
        "Maize": 16000
    }.get(crop, 15000)

    optimized_cost = base_cost * 0.85

    return {
        "normal_cost": round(base_cost * area, 2),
        "optimized_cost": round(optimized_cost * area, 2),
        "savings": round((base_cost - optimized_cost) * area, 2)
    }
