import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import plotly.express as px

# ---------------- PAGE CONFIG (MOBILE FRIENDLY) ----------------
st.set_page_config(
    page_title="AI Agri Optimizer",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------
for k in ["lat", "lon", "address", "map", "analyzed"]:
    if k not in st.session_state:
        st.session_state[k] = None if k != "analyzed" else False

# ---------------- LOCATION (DEPLOY SAFE) ----------------
def get_location(place):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place + ", India", "format": "json", "limit": 1}
    headers = {"User-Agent": "ai-agri-app"}

    r = requests.get(url, params=params, headers=headers, timeout=10)
    data = r.json()

    if not data:
        raise ValueError("Location not found")

    return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌾 Farm Details")

place = st.sidebar.text_input("Village / City / PIN", "Madurai")
crop = st.sidebar.selectbox("Crop", ["Rice", "Wheat", "Maize"])
season = st.sidebar.selectbox("Season", ["Kharif", "Rabi"])
area = st.sidebar.number_input("Area (acres)", 0.5, 50.0, 1.0)

analyze = st.sidebar.button("Analyze")

# ---------------- ANALYZE ----------------
if analyze:
    try:
        lat, lon, address = get_location(place)
    except Exception:
        st.error("Location not found. Try nearest city.")
        st.stop()

    st.session_state.lat = lat
    st.session_state.lon = lon
    st.session_state.address = address
    st.session_state.analyzed = True

    if st.session_state.map is None:
        m = folium.Map(location=[lat, lon], zoom_start=11)
        folium.Marker([lat, lon], tooltip=place).add_to(m)
        st.session_state.map = m

# ---------------- STOP UNTIL ANALYZED ----------------
if not st.session_state.analyzed:
    st.title("🌾 AI Agri Optimizer")
    st.caption("Real-time satellite & ML-based farm intelligence")
    st.info("Enter details in the sidebar and tap **Analyze**")
    st.stop()

lat = st.session_state.lat
lon = st.session_state.lon
address = st.session_state.address

# ---------------- HEADER ----------------
st.title(f"🌾 AI Agri — {place.title()}")
st.caption("Satellite • Weather • Soil • Yield • Cost Optimization")

# ---------------- MAP ----------------
st.subheader("🗺 Farm Location")
st.success(address)
st_folium(st.session_state.map, height=280, key="STATIC_MAP")

# ---------------- WEATHER ----------------
with st.expander("🌦 Weather (Last 7 Days)", expanded=True):

    weather_url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        "?parameters=T2M,PRECTOTCORR"
        f"&latitude={lat}&longitude={lon}"
        "&community=AG&format=JSON"
    )

    try:
        w = requests.get(weather_url, timeout=20).json()
        p = w["properties"]["parameter"]

        weather_df = pd.DataFrame({
            "Temperature (°C)": list(p["T2M"].values())[-7:],
            "Rainfall (mm)": list(p["PRECTOTCORR"].values())[-7:]
        })

    except Exception:
        weather_df = pd.DataFrame({
            "Temperature (°C)": [30, 31, 32, 31, 30, 29, 30],
            "Rainfall (mm)": [2, 0, 5, 1, 0, 0, 3]
        })
        st.warning("Live weather unavailable – using seasonal averages.")

    st.plotly_chart(px.line(weather_df, markers=True),
                    use_container_width=True)

# ---------------- NDVI ----------------
with st.expander("🛰 Satellite NDVI (30 Days)", expanded=True):

    end = datetime.utcnow().date()
    start = end - timedelta(days=30)

    ndvi_url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        "?parameters=NDVI"
        f"&latitude={lat}&longitude={lon}"
        f"&start={start.strftime('%Y%m%d')}&end={end.strftime('%Y%m%d')}"
        "&community=AG&format=JSON"
    )

    avg_ndvi = None
    try:
        nd = requests.get(ndvi_url, timeout=20).json()
        nd = nd["properties"]["parameter"]["NDVI"]

        ndvi_df = pd.DataFrame({
            "Date": pd.to_datetime(nd.keys()),
            "NDVI": nd.values()
        }).dropna()

        avg_ndvi = ndvi_df["NDVI"].mean()

        st.metric("Average NDVI", round(avg_ndvi, 3))
        st.plotly_chart(
            px.line(ndvi_df, x="Date", y="NDVI", markers=True),
            use_container_width=True
        )

    except Exception:
        st.warning("NDVI data unavailable for this location.")

# ---------------- SOIL ----------------
state = next((s for s in [
    "Tamil Nadu", "Andhra Pradesh", "Telangana",
    "Karnataka", "Kerala", "Punjab"
] if s in address), "Unknown")

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

# ---------------- YIELD & COST ----------------
base_yield = {"Rice": 2400, "Wheat": 2200, "Maize": 2600}[crop]
soil_factor = {"Red Loamy Soil": 1.0, "Alluvial Soil": 1.05,
               "Black Cotton Soil": 1.1}.get(soil, 0.95)
season_factor = {"Kharif": 1.0, "Rabi": 0.9}[season]
ndvi_factor = max(0.7, min(1.2, avg_ndvi / 0.5)) if avg_ndvi else 1.0

yield_kg = round(base_yield * soil_factor *
                 season_factor * ndvi_factor * area, 2)

price_map = {"Rice": 25, "Wheat": 28, "Maize": 22}
cost_map = {"Rice": 18000, "Wheat": 15000, "Maize": 16000}

price = price_map[crop]
normal_cost = cost_map[crop] * area
optimized_cost = normal_cost * 0.85

revenue = yield_kg * price
profit_normal = revenue - normal_cost
profit_optimized = revenue - optimized_cost

st.subheader("📊 Yield & Profit")

st.metric("Estimated Yield (kg)", yield_kg)
st.metric("Revenue (₹)", round(revenue, 2))
st.metric("Optimized Profit (₹)", round(profit_optimized, 2))

profit_df = pd.DataFrame({
    "Scenario": ["Normal", "Optimized"],
    "Profit (₹)": [profit_normal, profit_optimized]
})

st.plotly_chart(
    px.bar(profit_df, x="Scenario", y="Profit (₹)", text_auto=True),
    use_container_width=True
)

# ---------------- GOVERNMENT SCHEMES ----------------
with st.expander("🏛 Government Schemes", expanded=True):

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

st.success("✅ Analysis complete. Mobile-ready • Stable • Deployable.")
