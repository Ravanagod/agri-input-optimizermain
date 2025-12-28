# optimizer/cost_optimizer.py

def optimize_cost(area, soil):
    """
    Cost optimization based on soil type
    Returns normal vs optimized cost breakdown
    """

    # Base costs per acre (₹)
    normal_cost = {
        "seed": 1200 * area,
        "fertilizer": 3000 * area,
        "labour": 2000 * area,
        "irrigation": 1500 * area
    }

    # Soil-based fertilizer optimization
    if "Black" in soil or "Alluvial" in soil:
        fert_factor = 0.9
    elif "Sandy" in soil:
        fert_factor = 1.1
    else:
        fert_factor = 1.0

    optimized_cost = {
        "seed": normal_cost["seed"],
        "fertilizer": normal_cost["fertilizer"] * fert_factor,
        "labour": normal_cost["labour"] * 0.95,
        "irrigation": normal_cost["irrigation"] * 0.9
    }

    return {
        "normal_total": round(sum(normal_cost.values()), 2),
        "optimized_total": round(sum(optimized_cost.values()), 2),
        "normal_breakdown": normal_cost,
        "optimized_breakdown": optimized_cost
    }
