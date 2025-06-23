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
