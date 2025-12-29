import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Dummy training dataset (realistic agri logic)
data = {
    "crop": [0, 0, 1, 1, 2, 2],  # Rice=0, Wheat=1, Maize=2
    "soil": [0, 1, 0, 1, 0, 1],  # Loamy=0, Black=1
    "season": [0, 1, 0, 1, 0, 1],  # Kharif=0, Rabi=1
    "rain": [120, 80, 100, 60, 90, 70],
    "temp": [30, 25, 28, 22, 32, 26],
    "yield": [2400, 2100, 2200, 1900, 2600, 2300]
}

df = pd.DataFrame(data)

X = df.drop("yield", axis=1)
y = df["yield"]

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

joblib.dump(model, "ml/yield_model.pkl")
print("✅ Yield model trained and saved as yield_model.pkl")
