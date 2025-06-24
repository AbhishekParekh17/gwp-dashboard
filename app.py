import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- LOGIN SETUP ---
USERNAME = "Nathan"
PASSWORD = "Nathan@314159"

# Sidebar login
st.set_page_config(page_title="Surfboard GWP Insights", layout="wide")
st.sidebar.title("🔐 Login Required")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username != USERNAME or password != PASSWORD:
    st.sidebar.warning("Please enter correct credentials to continue.")
    st.stop()

# --- MAIN DASHBOARD ---
st.title("🌊 SwellCycle GWP Calculator Dashboard")
st.markdown("Welcome, **Nathan**. Explore the life cycle emissions of your surfboard below.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("📦 **Material Inputs**")
    st.info("This section allows user-defined values or default suggestions for PET, epoxy, etc.")

with col2:
    st.markdown("📊 **GWP Charts**")
    st.warning("Charts will appear here after input.")

st.markdown("---")

# -------------------------------
# Step 1: Material-Based Emissions Calculator
# -------------------------------
st.header("🧱 Step 1: Material-Based Emissions Calculator")

material_data = [
    {"Material": "PET Filament", "Unit": "kg", "Suggested EF": 3.468},
    {"Material": "Epoxy Resin", "Unit": "kg", "Suggested EF": 6.55},
    {"Material": "Fiberglass", "Unit": "kg", "Suggested EF": 2.63},
    {"Material": "Glassing", "Unit": "kg", "Suggested EF": 4.27},
    {"Material": "Testing", "Unit": "kWh", "Suggested EF": 0.198},
]

material_inputs = []

for i, row in enumerate(material_data):
    col1, col2, col3 = st.columns(3)
    name = col1.text_input(f"Name {i+1}", value=row["Material"])
    qty = col2.number_input(f"Quantity of {name} ({row['Unit']})", min_value=0.0, value=0.0)
    ef = col3.number_input(f"Emission Factor for {name} (kg CO₂ eq/{row['Unit']})", value=row["Suggested EF"])
    material_inputs.append({"Material": name, "Quantity": qty, "EF": ef})

material_results = []
for entry in material_inputs:
    total_gwp = entry["Quantity"] * entry["EF"]
    material_results.append({"Material": entry["Material"], "Total GWP (kg CO₂ eq)": round(total_gwp, 3)})

material_df = pd.DataFrame(material_results)
st.subheader("GWP Contribution Table")
st.dataframe(material_df)

if not material_df.empty and material_df["Total GWP (kg CO₂ eq)"].sum() > 0:
    st.subheader("GWP Contribution Pie Chart")
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        material_df["Total GWP (kg CO₂ eq)"],
        labels=material_df["Material"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)
elif not material_df.empty:
    st.info("Please enter non-zero values to display the pie chart.")


# -------------------------------
# Step 2: 3D Printing Energy GWP Calculator
# -------------------------------
st.header("🖨️ Step 2: 3D Printing Energy GWP Calculator")

try:
    hours = float(st.number_input("Enter total 3D printing hours", min_value=0.0, value=0.0))
    printer_power = float(st.number_input("Enter printer's power draw (kWh/hour)", value=1.2))
    solar_percent = float(st.number_input("% Solar Energy Used", value=20.0, min_value=0.0, max_value=100.0))
    grid_percent = 100.0 - solar_percent
    solar_ef = float(st.number_input("Emission Factor - Solar (kg CO₂ eq/kWh)", value=0.05))
    grid_ef = float(st.number_input("Emission Factor - Grid (kg CO₂ eq/kWh)", value=0.198))

    total_energy = hours * printer_power
    solar_energy = total_energy * (solar_percent / 100.0)
    grid_energy = total_energy * (grid_percent / 100.0)
    solar_emissions = solar_energy * solar_ef
    grid_emissions = grid_energy * grid_ef
    total_printing_gwp = solar_emissions + grid_emissions

    st.success(f"Total GWP from 3D Printing: {total_printing_gwp:.2f} kg CO₂ eq")

    st.bar_chart({"Solar": [solar_emissions], "Grid": [grid_emissions]})

except Exception as e:
    st.warning("⚠️ Please enter valid printing details.")

# -------------------------------
# Step 3: Transportation Emissions Calculator
# -------------------------------
st.header("🚚 Step 3: Transportation Emissions Calculator")

try:
    distance = float(st.number_input("Enter total transport distance (miles)", min_value=0.0, value=0.0))
    payload = float(st.number_input("Enter total transported weight (kg)", min_value=0.0, value=0.0))

    st.markdown("#### Contribution (%) by Transport Mode")
    road_share = float(st.number_input("Road (%)", min_value=0.0, max_value=100.0, value=25.0))
    sea_share = float(st.number_input("Sea (%)", min_value=0.0, max_value=100.0, value=25.0))
    air_share = float(st.number_input("Air (%)", min_value=0.0, max_value=100.0, value=25.0))
    rail_share = float(st.number_input("Rail (%)", min_value=0.0, max_value=100.0, value=25.0))

    if road_share + sea_share + air_share + rail_share != 100.0:
        st.warning("🚫 The transport mode percentages must add up to 100%.")
    else:
        # Emission factors (user-editable in future)
        road_ef = float(st.number_input("Road EF (kg CO₂ eq per kg-mile)", value=0.0000689))
        sea_ef = float(st.number_input("Sea EF (kg CO₂ eq per kg-mile)", value=0.0000123))
        air_ef = float(st.number_input("Air EF (kg CO₂ eq per kg-mile)", value=0.000785))
        rail_ef = float(st.number_input("Rail EF (kg CO₂ eq per kg-mile)", value=0.000045))

        # Weighted emissions
        road_gwp = distance * payload * road_ef * (road_share / 100.0)
        sea_gwp = distance * payload * sea_ef * (sea_share / 100.0)
        air_gwp = distance * payload * air_ef * (air_share / 100.0)
        rail_gwp = distance * payload * rail_ef * (rail_share / 100.0)
        total_transport_gwp = road_gwp + sea_gwp + air_gwp + rail_gwp

        st.success(f"Total Transportation GWP: {total_transport_gwp:.3f} kg CO₂ eq")

        chart_data = pd.DataFrame({
            "Mode": ["Road", "Sea", "Air", "Rail"],
            "GWP": [road_gwp, sea_gwp, air_gwp, rail_gwp]
        })
        st.bar_chart(chart_data.set_index("Mode"))

except Exception as e:
    st.warning("⚠️ Please enter valid transport inputs.")

# --- Footer ---
st.markdown("---")
st.markdown("© 2024 Abhishek Parekh. All rights reserved. This dashboard is IP protected.")
