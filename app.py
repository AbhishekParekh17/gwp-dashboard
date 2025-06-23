import streamlit as st

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

# --- MAIN DASHBOARD ---
st.set_page_config(page_title="Surfboard GWP Insights", layout="wide")
st.title("🌊 SwellCycle GWP Calculator Dashboard")
st.markdown("Welcome, **Nathan**. Explore the life cycle emissions of your surfboard below.")

# Sidebar form (to be expanded)
st.sidebar.markdown("## Input Parameters")
st.sidebar.text("➡️ More options coming soon...")

# Main dashboard placeholders
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("📦 **Material Inputs**")
    st.info("This section will show input sliders and default values for PET, epoxy, etc.")

with col2:
    st.markdown("📊 **GWP Charts**")
    st.warning("Charts will appear here after input.")

st.markdown("📋 **GWP Summary Table (Coming Soon)**")
.
.
.
.
#Module1 : Material & Process calculator

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample default emission factors and units
default_data = {
    "Material/Process": ["PET Filament", "Epoxy Resin", "Fiberglass", "3D Printing", "Glassing", "Testing"],
    "Unit": ["kg", "kg", "kg", "kWh", "kg", "kWh"],
    "Default Emission Factor": [3.468, 6.55, 2.63, 0.198, 4.27, 0.198],
}

df = pd.DataFrame(default_data)

st.title("Material & Process GWP Calculator")

# Input fields
st.header("Enter Quantities and Emission Factors")
user_inputs = []

for index, row in df.iterrows():
    col1, col2, col3 = st.columns(3)

    # Name validation
    name = col1.text_input(f"Name {index+1}", value=row["Material/Process"])
    if name.replace(" ", "").isdigit():
        st.warning(f"⚠️ Name for row {index+1} looks numeric — please enter a valid material/process name.")
        continue

    # Quantity input with validation
    try:
        qty = float(col2.text_input(f"Quantity of {name} ({row['Unit']})", value="0.0"))
    except ValueError:
        st.warning(f"⚠️ Please enter a number for quantity of {name}")
        qty = 0.0

    # Emission factor input with validation
    try:
        ef = float(col3.text_input(f"Emission Factor for {name} (kg CO₂ eq/unit)", value=str(row["Default Emission Factor"])))
    except ValueError:
        st.warning(f"⚠️ Please enter a number for emission factor of {name}")
        ef = 0.0

    user_inputs.append({
        "Material/Process": name,
        "Quantity": qty,
        "Emission Factor": ef
    })

# Output processing
results = []
for item in user_inputs:
    total_gwp = item["Quantity"] * item["Emission Factor"]
    results.append({"Material/Process": item["Material/Process"], "Total GWP (kg CO₂ eq)": round(total_gwp, 3)})

result_df = pd.DataFrame(results)

st.subheader("GWP Contribution Table")
st.dataframe(result_df)

# Chart
if not result_df.empty:
    st.subheader("GWP Contribution Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(result_df["Total GWP (kg CO₂ eq)"], labels=result_df["Material/Process"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
