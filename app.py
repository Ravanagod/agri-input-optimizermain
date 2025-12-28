import streamlit as st
import folium
import pandas as pd
import plotly.express as px

# ===== SERVICES =====
from services.location_service import get_coordinates
from services.weather_service import fetch_weather
from services.soil_service import get_soil_type
from services.scheme_service import get_schemes
from optimizer.yield_model import predict_yield

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Agri Optimizer",
    layout="wide",
    page_icon="🌾"
)

# =========================================================
# SESSION STATE (CRITICAL – NO FLASHING)
# =========================================================
if "map_html" not in st.session_state:
    st.session_state.map_html = None

if "results" not in st.session_state:
    st.session_state.results = None

# =========================================================
# MAP BUILDER (STABLE – BUILT ONCE)
# =========================================================
def build_map(lat, lon):
    m = folium.Map(
        location=[lat, lon],
        zoom_start=11,
        control_scale=True,
        tiles="OpenStreetMap"
    )

    folium.Marker(
        [lat, lon],
        tooltip="Farm Location",
        icon=folium.Icon(color="green", icon="leaf", prefix="fa")
    ).add_to(m)

    return m._repr_html_()

# =========================================================
# SIDEBAR INPUTS
# =========================================================
with st.sidebar:
    st.markdown("## 🌾 Farm Details")

    place = st.text_input("Village / City / PIN", "Madurai")
    crop = st.selectbox("Crop", ["Rice", "Wheat", "Maize"])
    season = st.selectbox("Season", ["Kharif", "Rabi"])
    area = st.number_input("Area (acres)", min_value=0.5, value=1.0, step=0.5)

    analyze = st.button("Analyze")

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <h1>AI Agri Optimizer</h1>
    <p style="color:gray">
    Location • Weather • Yield • Cost • Schemes
    </p>
    """,
    unsafe_allow_html=True
)

# =========================================================
# ANALYSIS (ONLY ON BUTTON CLICK)
# =========================================================
if analyze:
    coords = get_coordinates(place)

    if not coords:
        st.error("❌ Location not found. Try nearest town.")
        st.stop()

    lat, lon = coords

    # Weather
    weather_df = fetch_weather(lat, lon)

    # Soil
    soil = get_soil_type(place)

    # Yield (rule/ML-style)
    yield_kg = predict_yield(
        crop=crop,
        soil=soil,
        season=season,
        area=area,
        weather_df=weather_df
    )

    # Cost & revenue model
    cost_per_acre = {
        "Rice": 18000,
        "Wheat": 15000,
        "Maize": 16000
    }.get(crop, 16000)

    price_per_kg = {
        "Rice": 25,
        "Wheat": 22,
        "Maize": 20
    }.get(crop, 22)

    total_cost = cost_per_acre * area
    revenue = yield_kg * price_per_kg
    profit = revenue - total_cost

    # Save results
    st.session_state.map_html = build_map(lat, lon)
    st.session_state.results = {
        "place": place,
        "soil": soil,
        "yield": yield_kg,
        "cost": total_cost,
        "revenue": revenue,
        "profit": profit,
        "weather": weather_df
    }

# =========================================================
# MAP DISPLAY (NO FLASH)
# =========================================================
if st.session_state.map_html:
    st.markdown("## 🗺 Farm Location")
    st.components.v1.html(
        st.session_state.map_html,
        height=500,
        scrolling=False
    )

# =========================================================
# RESULTS
# =========================================================
if st.session_state.results:
    r = st.session_state.results

    # ---------- METRICS ----------
    st.markdown("## 📊 Key Metrics")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🌱 Soil Type", r["soil"])
    c2.metric("🌾 Yield (kg)", round(r["yield"], 1))
    c3.metric("💰 Revenue (₹)", int(r["revenue"]))
    c4.metric("📈 Profit (₹)", int(r["profit"]))

    # ---------- WEATHER ----------
    st.markdown("## 🌦 Weather (Last 5 Days)")
    st.dataframe(r["weather"].tail(5), use_container_width=True)

    fig_weather = px.line(
        r["weather"],
        x="Date",
        y="Temp_C",
        title="Temperature Trend (°C)"
    )
    st.plotly_chart(fig_weather, use_container_width=True)

    # ---------- YIELD / COST / PROFIT CHART ----------
    st.markdown("## 📈 Yield, Cost & Profit")

    chart_df = pd.DataFrame({
        "Metric": ["Yield (kg)", "Cost (₹)", "Revenue (₹)", "Profit (₹)"],
        "Value": [
            r["yield"],
            r["cost"],
            r["revenue"],
            r["profit"]
        ]
    })

    fig_bar = px.bar(
        chart_df,
        x="Metric",
        y="Value",
        title="Yield, Cost & Profit Comparison"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ---------- GOVERNMENT SCHEMES ----------
    st.markdown("## 🏛 Government Schemes (State-based)")
    schemes = get_schemes(r["place"], crop)
    for s in schemes:
        st.success(s)

    # ---------- AI ADVISORY ----------
    st.markdown("## 🧠 AI Advisory")

    if r["profit"] < 0:
        st.error(
            "Loss detected.\n"
            "- Reduce input costs\n"
            "- Consider crop or season change"
        )
    elif r["yield"] < 2000:
        st.warning(
            "Yield below optimal.\n"
            "- Improve irrigation\n"
            "- Check nutrient management"
        )
    else:
        st.success(
            "Crop outlook is good.\n"
            "- Maintain current practices\n"
            "- Monitor weather regularly"
        )

else:
    st.info("👈 Enter farm details and click **Analyze**")
