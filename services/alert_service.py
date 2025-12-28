def generate_alerts(temp, rainfall, predicted_profit):
    alerts=[]
    if temp > 38:
        alerts.append("Extreme heat risk — consider mulching/irrigation scheduling.")
    if rainfall < 300:
        alerts.append("Low rainfall — plan irrigation or drought resilient crops.")
    if predicted_profit < 0:
        alerts.append("Expected loss — review inputs or crop choice.")
    return alerts
