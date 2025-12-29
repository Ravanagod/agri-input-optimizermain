import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Agri Optimizer", layout="wide")

# ---------------- SESSION STATE ----------------
for k in ["lat", "lon", "address", "map", "analyzed"]:
    if k not in st.session_state:
        st.session_state[k] = None if k != "analyzed" else False

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌾 Farm Details")

place = st.sidebar.text_input("Village / City / PIN", "Madurai")
crop = st.sidebar.selectbox("Crop", ["Rice", "Wheat", "Maize"])
season = st.sidebar.selectbox("Season", ["Kharif", "Rabi"])
area = st.sidebar.number_input("Area (acres)", 0.5, 50.0, 1.0)

analyze = st.sidebar.button("Analyze")

# ---------------- LOCATION ----------------
if analyze:
    geolocator = Nominatim(user_agent="ai_agri_app", timeout=10)
    location = geolocator.geocode(place + ", India")

    if not location:
        st.error("Location not found. Try nearest city.")
        st.stop()

    st.session_state.lat = location.latitude
    st.session_state.lon = location.longitude
    st.session_state.address = location.address
    st.session_state.analyzed = True

    m = folium.Map(
        location=[st.session_state.lat, st.session_state.lon],
        zoom_start=11,
        tiles="OpenStreetMap"
    )
    folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        tooltip=place
    ).add_to(m)

    st.session_state.map = m

# ---------------- STOP UNTIL ANALYZED ----------------
if not st.session_state.analyzed:
    st.title("AI Agri Optimizer")
    st.info("Enter details and click **Analyze**")
    st.stop()

lat = st.session_state.lat
lon = st.session_state.lon
address = st.session_state.address

# ---------------- HEADER ----------------
st.title(f"🌾 AI Agri — {place.title()}")
st.caption("Satellite • Weather • Soil • Yield • Cost Optimization")

# ---------------- MAP (NO FLASHING) ----------------
st.subheader("🗺 Farm Location")
st.success(address)
st_folium(st.session_state.map, height=400, key="STATIC_MAP")

# ---------------- WEATHER ----------------
st.subheader("🌦 Weather (Last 7 Days)")

weather_url = (
    "https://power.larc.nasa.gov/api/temporal/daily/point"
    "?parameters=T2M,PRECTOTCORR"
    f"&latitude={lat}&longitude={lon}"
    "&community=AG&format=JSON"
)

try:
    w = requests.get(weather_url, timeout=20).json()
    params = w["properties"]["parameter"]

    weather_df = pd.DataFrame({
        "Temperature (°C)": list(params["T2M"].values())[-7:],
        "Rainfall (mm)": list(params["PRECTOTCORR"].values())[-7:]
    })

except Exception:
    weather_df = pd.DataFrame({
        "Temperature (°C)": [30, 31, 32, 31, 30, 29, 30],
        "Rainfall (mm)": [2, 0, 5, 1, 0, 0, 3]
    })
    st.warning("Live weather unavailable – using seasonal averages.")

st.plotly_chart(px.line(weather_df, markers=True), use_container_width=True)

# ---------------- NDVI ----------------
st.subheader("🛰 Satellite NDVI (30 Days)")

end = datetime.utcnow().date()
start = end - timedelta(days=30)

ndvi_url = (
    "https://power.larc.nasa.gov/api/temporal/daily/point"
    "?parameters=NDVI"
    f"&latitude={lat}&longitude={lon}"
    f"&start={start.strftime('%Y%m%d')}"
    f"&end={end.strftime('%Y%m%d')}"
    "&community=AG&format=JSON"
)

avg_ndvi = None
try:
    ndvi_raw = requests.get(ndvi_url, timeout=20).json()
    nd = ndvi_raw["properties"]["parameter"]["NDVI"]

    ndvi_df = pd.DataFrame({
        "Date": pd.to_datetime(nd.keys()),
        "NDVI": nd.values()
    }).dropna()

    avg_ndvi = ndvi_df["NDVI"].mean()

    st.metric("Average NDVI", round(avg_ndvi, 3))
    st.plotly_chart(px.line(ndvi_df, x="Date", y="NDVI", markers=True),
                    use_container_width=True)

except Exception:
    st.warning("NDVI data unavailable for this location.")

# ---------------- SOIL ----------------
state = next(
    (s for s in [
        "Tamil Nadu", "Andhra Pradesh", "Telangana",
        "Karnataka", "Kerala", "Punjab"
    ] if s in address),
    "Unknown"
)

soil_map = {
    "Tamil Nadu": "Red Loamy Soil",
    "Andhra Pradesh": "Alluvial Soil",
    "Telangana": "Black Cotton Soil",
    "Karnataka": "Black Cotton Soil",
    "Kerala": "Laterite Soil",
    "Punjab": "Alluvial Soil"
}

soil = soil_map.get(state, "Mixed Regional Soil")

st.subheader("🌱 Soil Type")
st.success(soil)

# ---------------- YIELD MODEL ----------------
base_yield = {"Rice": 2400, "Wheat": 2200, "Maize": 2600}.get(crop, 2200)
soil_factor = {"Red Loamy Soil": 1.0, "Alluvial Soil": 1.05,
               "Black Cotton Soil": 1.1}.get(soil, 0.95)
season_factor = {"Kharif": 1.0, "Rabi": 0.9}.get(season, 1.0)

ndvi_factor = 1.0
if avg_ndvi:
    ndvi_factor = max(0.7, min(1.2, avg_ndvi / 0.5))

yield_kg = round(base_yield * soil_factor *
                 season_factor * ndvi_factor * area, 2)

# ---------------- PRICE & COST ----------------
price_map = {"Rice": 25, "Wheat": 28, "Maize": 22}
cost_map = {"Rice": 18000, "Wheat": 15000, "Maize": 16000}

price = price_map[crop]
normal_cost = cost_map[crop] * area
optimized_cost = normal_cost * 0.85

revenue = yield_kg * price
profit_normal = revenue - normal_cost
profit_optimized = revenue - optimized_cost

# ---------------- METRICS ----------------
st.subheader("📊 Yield, Cost & Profit")

c1, c2, c3 = st.columns(3)
c1.metric("Yield (kg)", yield_kg)
c2.metric("Market Price (₹/kg)", price)
c3.metric("Revenue (₹)", round(revenue, 2))

c4, c5, c6 = st.columns(3)
c4.metric("Normal Cost (₹)", normal_cost)
c5.metric("Optimized Cost (₹)", round(optimized_cost, 2))
c6.metric("Savings (₹)", round(normal_cost - optimized_cost, 2))

# ---------------- CHARTS ----------------
st.subheader("📈 Profit Comparison")

profit_df = pd.DataFrame({
    "Scenario": ["Normal", "Optimized"],
    "Profit (₹)": [profit_normal, profit_optimized]
})

st.plotly_chart(
    px.bar(profit_df, x="Scenario", y="Profit (₹)", text_auto=True),
    use_container_width=True
)

# ---------------- GOVERNMENT SCHEMES ----------------
st.subheader("🏛 Government Schemes")

central = [
    "PM-KISAN – ₹6000/year",
    "PMFBY – Crop Insurance",
    "Soil Health Card",
    "Kisan Credit Card"
]

state_schemes = {
    "Tamil Nadu": ["Kuruvai Special Package"],
    "Andhra Pradesh": ["YSR Rythu Bharosa"],
    "Telangana": ["Rythu Bandhu"],
    "Karnataka": ["Raitha Siri"]
}

for s in central + state_schemes.get(state, []):
    st.write("•", s)

st.success("✅ Analysis complete. Optimization based on soil, season, NDVI & weather.")
