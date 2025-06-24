import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# --- PAGE CONFIG & DARK THEME STYLE ---
st.set_page_config(page_title="🌊 SwellCycle GWP Dashboard", layout="wide")
from PIL import Image

# --- LOGO SETUP ---
logo = Image.open("swellcycle_logo.png")
st.image(logo, width=180)  # Adjust width as needed

st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .element-container:has(.stButton) button {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.5em;
    }
    .css-1aumxhk, .css-1v3fvcr {
        background-color: #262730 !important;
        color: white !important;
        border-radius: 8px;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN SETUP ---
USERNAME = "Nathan"
PASSWORD = "Nathan@314159"

st.sidebar.title("🔐 Login Required")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username != USERNAME or password != PASSWORD:
    st.sidebar.warning("Please enter correct credentials to continue.")
    st.stop()

# --- HEADER ---
st.title("🌊 SwellCycle GWP Insights Dashboard")
st.markdown("Track and visualize the carbon footprint of your surfboard production process in real time.")

# --- SUMMARY PLACEHOLDER ---
sum_materials = 0
sum_processes = 0
sum_transport = 0

# -----------------------------
# Step 1: Materials
# -----------------------------
st.markdown("## 🧱 Step 1: Material-Based GWP")
material_data = [
    {"Material": "PET Filament", "Unit": "kg", "Suggested EF": 3.468},
    {"Material": "Epoxy Resin", "Unit": "kg", "Suggested EF": 6.55},
    {"Material": "Fiberglass", "Unit": "kg", "Suggested EF": 2.63},
]

material_inputs = []
for i, row in enumerate(material_data):
    col1, col2, col3 = st.columns(3)
    name = col1.text_input(f"Name {i+1}", value=row["Material"])
    qty = col2.number_input(f"Quantity of {name} ({row['Unit']})", min_value=0.0, value=0.0)
    ef = col3.number_input(f"EF for {name} (kg CO₂ eq/{row['Unit']})", value=row["Suggested EF"], format="%.5f")
    material_inputs.append({"Material": name, "Quantity": qty, "EF": ef})

material_results = []
for entry in material_inputs:
    total_gwp = entry["Quantity"] * entry["EF"]
    material_results.append({"Material": entry["Material"], "Total GWP (kg CO₂ eq)": round(total_gwp, 3)})

material_df = pd.DataFrame(material_results)
sum_materials = material_df["Total GWP (kg CO₂ eq)"].sum()
st.success(f"Total Material GWP: {sum_materials:.2f} kg CO₂ eq")
st.dataframe(material_df)

if sum_materials > 0:
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.pie(material_df["Total GWP (kg CO₂ eq)"], labels=material_df["Material"], autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

# -----------------------------
# Step 2: Process Emissions
# -----------------------------
st.markdown("## ⚙️ Step 2: Process GWP (3D Printing, Glassing, Testing)")
try:
    hours = st.number_input("3D Printing Hours", min_value=0.0, value=0.0)
    printer_power = st.number_input("Printer Power (kWh/hour)", value=1.2)
    solar_percent = st.number_input("% Solar Used", value=20.0)
    grid_percent = 100.0 - solar_percent
    solar_ef = st.number_input("Solar EF (kg CO₂ eq/kWh)", value=0.05, format="%.5f")
    grid_ef = st.number_input("Grid EF (kg CO₂ eq/kWh)", value=0.198, format="%.5f")

    total_energy = hours * printer_power
    solar_energy = total_energy * (solar_percent / 100.0)
    grid_energy = total_energy * (grid_percent / 100.0)
    solar_emissions = solar_energy * solar_ef
    grid_emissions = grid_energy * grid_ef
    total_printing_gwp = solar_emissions + grid_emissions

    testing_energy = st.number_input("Testing Energy (kWh)", value=0.125)
    testing_ef = st.number_input("Testing EF (kg CO₂ eq/kWh)", value=0.198, format="%.5f")
    testing_gwp = testing_energy * testing_ef

    glassing_gwp = st.number_input("Fixed Glassing GWP (kg CO₂ eq)", value=4.27)

    process_df = pd.DataFrame({
        "Process": ["3D Printing", "Testing", "Glassing"],
        "GWP (kg CO₂ eq)": [total_printing_gwp, testing_gwp, glassing_gwp]
    })

    sum_processes = process_df["GWP (kg CO₂ eq)"].sum()
    st.success(f"Total Process GWP: {sum_processes:.2f} kg CO₂ eq")
    st.dataframe(process_df)

    fig2, ax2 = plt.subplots(figsize=(5, 3))
    bars = ax2.bar(process_df["Process"], process_df["GWP (kg CO₂ eq)"], color="#A3C9A8")
    for i, v in enumerate(process_df["GWP (kg CO₂ eq)"]):
        ax2.text(i, v + 0.1, f"{v:.2f}", ha='center', color='white')
    st.pyplot(fig2)
except:
    st.warning("Please fill all process inputs.")

# -----------------------------
# Step 3: Transportation
# -----------------------------
st.markdown("## 🚚 Step 3: Transportation GWP")
try:
    distance = st.number_input("Transport Distance (miles)", min_value=0.0, value=0.0)
    payload = st.number_input("Transport Payload (kg)", min_value=0.0, value=0.0)

    road_pct = st.number_input("Road (%)", value=25.0)
    sea_pct = st.number_input("Sea (%)", value=25.0)
    air_pct = st.number_input("Air (%)", value=25.0)
    rail_pct = st.number_input("Rail (%)", value=25.0)

    if sum([road_pct, sea_pct, air_pct, rail_pct]) != 100:
        st.warning("Transport mode percentages must sum to 100%.")
    else:
        road_ef = st.number_input("Road EF (kg CO₂/kg-mile)", value=0.0000689, format="%.7f")
        sea_ef = st.number_input("Sea EF (kg CO₂/kg-mile)", value=0.0000123, format="%.7f")
        air_ef = st.number_input("Air EF (kg CO₂/kg-mile)", value=0.0007850, format="%.7f")
        rail_ef = st.number_input("Rail EF (kg CO₂/kg-mile)", value=0.0000450, format="%.7f")

        road_gwp = distance * payload * road_ef * (road_pct / 100.0)
        sea_gwp = distance * payload * sea_ef * (sea_pct / 100.0)
        air_gwp = distance * payload * air_ef * (air_pct / 100.0)
        rail_gwp = distance * payload * rail_ef * (rail_pct / 100.0)
        sum_transport = road_gwp + sea_gwp + air_gwp + rail_gwp

        st.success(f"Total Transport GWP: {sum_transport:.3f} kg CO₂ eq")

        df_transport = pd.DataFrame({
            "Mode": ["Road", "Sea", "Air", "Rail"],
            "GWP": [road_gwp, sea_gwp, air_gwp, rail_gwp]
        })
        fig3, ax3 = plt.subplots(figsize=(6, 3))
        barz = ax3.barh(df_transport["Mode"], df_transport["GWP"], color=['#90E0EF', '#FFB4A2', '#A3C4F3', '#B5E48C'])
        for bar in barz:
            ax3.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2, f"{bar.get_width():.2f}", va='center', color='white')
        st.pyplot(fig3)
        # --- 📥 DOWNLOAD BUTTON ---
summary_df = pd.DataFrame({
    "Component": ["Materials", "Processes", "Transportation"],
    "Total GWP (kg CO₂ eq)": [sum_materials, sum_processes, sum_transport]
})
# --- 📥 DOWNLOAD BUTTON ---
if not summary_df.empty:
    csv = summary_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download GWP Summary as CSV",
        data=csv,
        file_name="gwp_summary_swellcycle.csv",
        mime="text/csv"
    )


except:
    st.warning("Please complete transport fields.")
#

# -----------------------------
# FINAL SUMMARY
# -----------------------------
st.markdown("---")
total_gwp = sum_materials + sum_processes + sum_transport
st.header("📊 Final GWP Summary")
st.metric(label="Total GWP (kg CO₂ eq)", value=f"{total_gwp:.2f}")
st.caption("© 2024 Abhishek Parekh. All rights reserved.")
