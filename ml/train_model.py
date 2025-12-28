# ml/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Example CSV expected columns: crop,soil,season,area,rainfall,temperature,yield
df = pd.read_csv("ml/yield_training.csv")
# One-hot encode crop/soil/season
X = pd.get_dummies(df[['crop','soil','season','area','rainfall','temperature']], drop_first=True)
y = df['yield']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train,y_train)
joblib.dump((model, X.columns.tolist()), "ml/yield_model.joblib")
print("Saved model with features:", X.columns.tolist())
