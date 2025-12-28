import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Synthetic but realistic agri dataset
np.random.seed(42)

data = pd.DataFrame({
    "rainfall_mm": np.random.uniform(300, 1200, 500),
    "temperature_c": np.random.uniform(18, 38, 500),
    "soil_code": np.random.randint(1, 6, 500),
    "season_code": np.random.randint(1, 4, 500),
    "area_acres": np.random.uniform(0.5, 5, 500)
})

# Yield logic (ground truth approximation)
data["yield_kg"] = (
    data["rainfall_mm"] * 1.2 +
    (35 - data["temperature_c"]) * 40 +
    data["soil_code"] * 180 +
    data["season_code"] * 120
) * data["area_acres"]

X = data.drop("yield_kg", axis=1)
y = data["yield_kg"]

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "ml/yield_model.pkl")
print("✅ Yield model trained & saved")
