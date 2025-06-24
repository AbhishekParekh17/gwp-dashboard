import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- LOGIN SETUP ---
USERNAME = "Nathan"
PASSWORD = "Nathan@314159"

# Sidebar login
st.sidebar.title("🔐 Login Required")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username != USERNAME or password != PASSWORD:
    st.sidebar.warning("Please enter correct credentials to continue.")
    st.stop()

# --- MAIN PAGE SETUP ---
st.set_page_config(page_title="Surfboard GWP Insights", layout="wide")
st.title("🌊 SwellCycle GWP Calculator Dashboard")
st.markdown("Welcome, **Nathan**. Explore the life cycle emissions of your surfboard below.")

# --- Sidebar section ---
st.sidebar.markdown("## Input Parameters")
st.sidebar.text("➡️ More options coming soon...")

# --- Columns for layout ---
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("📦 **Material Inputs**")
    st.info("This section allows input for materials used in surfboard manufacturing.")

with col2:
    st.markdown("📊 **GWP Charts**")
    st.warning("Charts will appear here after input.")

# --- Material GWP Calculator (Module 1) ---
st.markdown("## 🔧 Step 1: Material-Based Emissions Calculator")

material_data = {
    "Material/Process": ["PET Filament", "Epoxy Resin", "Fiberglass"],
    "Unit": ["kg", "kg", "kg"],
    "Suggested EF (kg CO₂ eq/unit)": [3.468, 6.55, 2.63]
}

df = pd.DataFrame(material_data)
material_inputs = []

for i, row in df.iterrows():
    col1, col2, col3 = st.columns(3)

    name = col1.text_input(f"Name {i+1}", value=row["Material/Process"])
    
    try:
        qty = float(col2.text_input(f"Quantity of {name} ({row['Unit']})", value="0.0"))
    except ValueError:
        st.warning(f"Please enter a valid number for quantity of {name}")
        qty = 0.0

    ef = col3.number_input(
        f"Emission Factor for {name} (kg CO₂ eq/unit)",
        value=row["Suggested EF (kg CO₂ eq/unit)"],
        min_value=0.0,
        help="Suggested value shown, but feel free to enter your own"
    )

    material_inputs.append({
        "Material/Process": name,
        "Quantity": qty,
        "Emission Factor": ef
    })

# Add fixed values for Glassing and Testing
material_inputs.append({
    "Material/Process": "Glassing",
    "Quantity": 1,
    "Emission Factor": st.number_input("Emission Factor for Glassing (kg CO₂ eq)", value=4.27, min_value=0.0)
})
material_inputs.append({
    "Material/Process": "Testing",
    "Quantity": 1,
    "Emission Factor": st.number_input("Emission Factor for Testing (kg CO₂ eq)", value=0.198, min_value=0.0)
})

# Calculate Material GWP
results = []
for item in material_inputs:
    total_gwp = item["Quantity"] * item["Emission Factor"]
    results.append({
        "Material/Process": item["Material/Process"],
        "Total GWP (kg CO₂ eq)": round(total_gwp, 3)
    })

df_results = pd.DataFrame(results)

st.subheader("📋 GWP Contribution Table")
st.dataframe(df_results)

# Pie Chart
if not df_results.empty:
    st.subheader("🧁 GWP Contribution Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(
        df_results["Total GWP (kg CO₂ eq)"],
        labels=df_results["Material/Process"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

# --- 3D Printing GWP Calculator (Module 2) ---
st.markdown("---")
st.markdown("## 🖨️ Step 2: 3D Printing Energy GWP Calculator")

try:
    hours = st.number_input("Enter total 3D printing hours", min_value=0.0, step=1.0)

    solar_pct = st.slider("Solar Energy Contribution (%)", min_value=0, max=100, value=20)
    grid_pct = 100 - solar_pct
    st.markdown(f"**Grid Energy Contribution:** {grid_pct}%")

    use_suggested = st.radio("Use suggested emission factors?", ["Yes", "No"], horizontal=True)

    if use_suggested == "Yes":
        solar_ef = 0.05
        grid_ef = 0.198
    else:
        solar_ef = st.number_input("Enter Solar Emission Factor (kg CO₂ eq/kWh)", min_value=0.0)
        grid_ef = st.number_input("Enter Grid Emission Factor (kg CO₂ eq/kWh)", min_value=0.0)

    power_draw = st.number_input("Enter printer's energy draw (kWh/hour)", value=1.2, min_value=0.0)

    total_energy = power_draw * hours
    solar_energy = total_energy * (solar_pct / 100)
    grid_energy = total_energy * (grid_pct / 100)

    solar_emissions = solar_energy * solar_ef
    grid_emissions = grid_energy * grid_ef
    total_3dp_gwp = round(solar_emissions + grid_emissions, 3)

    st.success(f"Total GWP from 3D Printing: **{total_3dp_gwp} kg CO₂ eq**")

    st.subheader("🔋 3D Printing Energy Emission Breakdown")
    st.bar_chart({
        "Solar Energy": [solar_emissions],
        "Grid Energy": [grid_emissions]
    })

except Exception as e:
    st.warning("⚠️ Please ensure all 3D printing fields are correctly filled.")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 Abhishek Parekh. All rights reserved. This dashboard is IP protected.")
#
#
#
#
# --------------------------------------
# Step 3 – Multi-Mode Transportation GWP Calculator
# --------------------------------------
st.markdown("---")
st.markdown("### 🚚 Step 3: Transportation Emissions Calculator (Multi-Mode)")

st.info("Enter total distance, payload, emission factors, and energy mode distribution for transport (Road / Sea / Air).")

try:
    distance = float(st.number_input("Enter total transport distance (miles)", min_value=0.0, value=100.0))
    payload = float(st.number_input("Enter total payload (kg)", min_value=0.0, value=10.0))

    st.markdown("#### 🚛 Transport Mode Split (in %)")
    road_percent = st.slider("Road (%)", 0, 100, 50)
    sea_percent = st.slider("Sea (%)", 0, 100 - road_percent, 30)
    air_percent = 100 - road_percent - sea_percent

    st.markdown(f"**Air (%)**: {air_percent}")

    use_default_transport_ef = st.radio("Use suggested emission factors?", ["Yes", "No"])

    if use_default_transport_ef == "Yes":
        road_ef = 0.0000689
        sea_ef = 0.000012  # Suggestion, can be adjusted later
        air_ef = 0.000505
    else:
        road_ef = float(st.number_input("Enter Road EF (kg CO₂ eq per kg-mile)", min_value=0.0, value=0.0000689))
        sea_ef = float(st.number_input("Enter Sea EF (kg CO₂ eq per kg-mile)", min_value=0.0, value=0.000012))
        air_ef = float(st.number_input("Enter Air EF (kg CO₂ eq per kg-mile)", min_value=0.0, value=0.000505))

    # Calculate weighted transport emissions
    road_gwp = payload * distance * road_ef * (road_percent / 100)
    sea_gwp = payload * distance * sea_ef * (sea_percent / 100)
    air_gwp = payload * distance * air_ef * (air_percent / 100)

    total_transport_gwp = road_gwp + sea_gwp + air_gwp

    st.success(f"Total GWP from transportation: **{total_transport_gwp:.3f} kg CO₂ eq**")

    st.bar_chart({
        "Mode": ["Road", "Sea", "Air"],
        "GWP (kg CO₂ eq)": [road_gwp, sea_gwp, air_gwp]
    })

except Exception as e:
    st.warning("⚠️ Please check the values entered in the transport section.")
