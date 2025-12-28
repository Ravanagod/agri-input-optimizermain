import joblib
import pandas as pd
import datetime

model, le_crop, le_mandi = joblib.load("models/price_model.pkl")

def predict_price(crop, mandi, days=7):
    today = datetime.date.today()
    preds = []

    for i in range(1, days + 1):
        future = today + datetime.timedelta(days=i)
        X = pd.DataFrame([{
            "day": future.day,
            "month": future.month,
            "crop_enc": le_crop.transform([crop])[0],
            "mandi_enc": le_mandi.transform([mandi])[0]
        }])
        price = model.predict(X)[0]
        preds.append((future, price))

    return preds
