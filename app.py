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

# Page layout
st.set_page_config(page_title="Surfboard GWP Insights", layout="wide")
st.title("🌊 SwellCycle GWP Calculator Dashboard")
st.markdown("Welcome, **Nathan**. Explore the life cycle emissions of your surfboard below.")

# Section Headers
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("📦 **Material Inputs**")
    st.info("Enter quantities and emission factors for materials and processes. Suggested values are shown below each field.")

with col2:
    st.markdown("📊 **GWP Charts**")
    st.warning("Charts will appear here after input.")

st.markdown("📋 **GWP Summary Table (Coming Soon)**")

# --- MODULE 1: MATERIAL AND PROCESS INPUTS ---

material_data = [
    {"name": "PET Filament", "unit": "kg", "suggested_ef": 3.468},
    {"name": "Epoxy Resin", "unit": "kg", "suggested_ef": 6.55},
    {"name": "Fiberglass", "unit": "kg", "suggested_ef": 2.63},
]

process_data = [
    {"name": "Glassing", "quantity": 1.0, "unit": "kg", "suggested_ef": 4.27},
    {"name": "Testing", "quantity": 0.125, "unit": "kWh", "suggested_ef": 0.198},
]

user_material_inputs = []

st.subheader("🔧 Step 1: Material & Process Inputs")

for item in material_data:
    with st.expander(f"{item['name']}"):
        name = item["name"]
        try:
            qty = float(st.number_input(f"Quantity of {name} ({item['unit']})", min_value=0.0))
        except:
            qty = 0.0
        ef = st.number_input(
            f"Emission Factor for {name} (kg CO₂ eq per {item['unit']})",
            min_value=0.0,
            help=f"Suggested: {item['suggested_ef']}"
        )
        user_material_inputs.append({
            "Material/Process": name,
            "Quantity": qty,
            "EF": ef,
            "Total GWP": qty * ef
        })

# Glassing & Testing - fixed quantity, user-supplied EF
for proc in process_data:
    with st.expander(f"{proc['name']}"):
        ef = st.number_input(
            f"Emission Factor for {proc['name']} (kg CO₂ eq per {proc['unit']})",
            min_value=0.0,
            help=f"Suggested: {proc['suggested_ef']}"
        )
        user_material_inputs.append({
            "Material/Process": proc['name'],
            "Quantity": proc['quantity'],
            "EF": ef,
            "Total GWP": proc['quantity'] * ef
        })

# --- MODULE 2: 3D PRINTING ENERGY ---

st.subheader("🖨️ Step 2: 3D Printing Energy GWP Calculator")

try:
    hours = float(st.number_input("Enter 3D Printing Time (in hours)", min_value=1.0, step=1.0))
    power_draw = st.number_input("Printer Power Consumption (kWh per hour)", min_value=0.0, value=1.2)
    total_energy = hours * power_draw

    solar_pct = float(st.slider("Solar Energy Share (%)", min_value=0, max_value=100, value=20))
    grid_pct = 100 - solar_pct
    st.markdown(f"🔌 **Grid Share**: {grid_pct}%")

    solar_ef = st.number_input(
        "Emission Factor for Solar (kg CO₂ eq/kWh)",
        min_value=0.0,
        help="Suggested: 0.05"
    )
    grid_ef = st.number_input(
        "Emission Factor for Grid (kg CO₂ eq/kWh)",
        min_value=0.0,
        help="Suggested: 0.198"
    )

    solar_energy = total_energy * (solar_pct / 100)
    grid_energy = total_energy * (grid_pct / 100)

    solar_emission = solar_energy * solar_ef
    grid_emission = grid_energy * grid_ef
    total_3dp_emission = solar_emission + grid_emission

    # Add to main list
    user_material_inputs.append({
        "Material/Process": "3D Printing (Energy)",
        "Quantity": total_energy,
        "EF": f"{solar_ef}/{grid_ef}",
        "Total GWP": total_3dp_emission
    })

    st.success(f"Total GWP from 3D Printing Energy: **{total_3dp_emission:.2f} kg CO₂ eq**")
    st.bar_chart({
        "Energy Type": ["Solar", "Grid"],
        "GWP (kg CO₂ eq)": [solar_emission, grid_emission]
    })

except Exception as e:
    st.warning("⚠️ Please enter valid numeric values.")

# --- SUMMARY TABLE AND PIE CHART ---

st.subheader("📈 Summary Table of All Contributions")

final_df = pd.DataFrame(user_material_inputs)
final_df_display = final_df[["Material/Process", "Quantity", "EF", "Total GWP"]]
st.dataframe(final_df_display)

# Pie chart of total GWP contribution
if not final_df.empty:
    st.subheader("📊 Total GWP Contribution Breakdown")
    fig, ax = plt.subplots()
    ax.pie(final_df["Total GWP"], labels=final_df["Material/Process"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
