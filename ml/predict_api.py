# ml/predict_api.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()
model, feat_cols = joblib.load("ml/yield_model.joblib")

class InputRow(BaseModel):
    crop: str
    soil: str
    season: str
    area: float
    rainfall: float
    temperature: float

@app.post("/predict")
def predict(row: InputRow):
    d = row.dict()
    df = pd.DataFrame([d])
    # one-hot to match training features
    df_enc = pd.get_dummies(df, drop_first=True)
    for c in feat_cols:
        if c not in df_enc.columns:
            df_enc[c]=0
    df_enc = df_enc[feat_cols]
    y_pred = model.predict(df_enc)[0]
    return {"predicted_yield": float(y_pred)}
