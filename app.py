import streamlit as st
import yaml
import os

# ----------------------------
# Load YAML configuration
# ----------------------------
CONFIG_FILE = "nbfc-credit-visibility-config.yaml"

if not os.path.exists(CONFIG_FILE):
    st.error("YAML configuration file not found.")
    st.stop()

with open(CONFIG_FILE, "r") as f:
    config = yaml.safe_load(f)

# ----------------------------
# Mock Credit Scoring Logic
# ----------------------------
bureau_score = 720
internal_score = 680

bureau_weight = config["composite_risk_score"]["bureau_weight"]
internal_weight = config["composite_risk_score"]["internal_weight"]

final_score = int(
    bureau_weight * bureau_score +
    internal_weight * internal_score
)

risk_label = "Unknown"
risk_color = "#999999"

for band in config["visualization_rules"]["score_bands"]:
    if band["min"] <= final_score <= band["max"]:
        risk_label = band["label"]
        risk_color = band["color"]
        break

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(
    page_title="NBFC Credit Risk Dashboard",
    layout="centered"
)

st.title("NBFC Credit Risk Dashboard")

st.metric("Composite Credit Score", final_score)

st.markdown(
    f"""
    <div style="
        margin-top:20px;
        padding:16px;
        background:{risk_color};
        color:white;
        font-size:18px;
        border-radius:8px;
        text-align:center;
        ">
        {risk_label}
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Enterprise NBFC Demo • YAML-Driven • Streamlit Cloud Safe")
