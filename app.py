import streamlit as st
from engine import run_credit_flow
from utils.yaml_loader import load_yaml

st.set_page_config(page_title="NBFC Credit Visibility", layout="wide")

config = load_yaml("nbfc-credit-visibility-config.yaml")

st.title("🏦 NBFC Credit Risk Visibility Dashboard")

# ---------------- INPUT PANEL ----------------
with st.sidebar:
    st.header("Applicant Inputs")

    bureau_score = st.slider("Bureau Score", 300, 900, 650)
    internal_score = st.slider("Internal Score", 300, 900, 620)
    overdue_days = st.number_input("Overdue Days", 0, 180, 0)
    emi_to_income = st.slider("EMI to Income %", 0, 100, 40)
    device_risk = st.selectbox("Device Risk", ["low", "medium", "high"])

    run = st.button("Run Credit Decision")

# ---------------- PROCESS ----------------
if run:
    result = run_credit_flow(
        config,
        {
            "bureau_score": bureau_score,
            "internal_score": internal_score,
            "overdue_days": overdue_days,
            "emi_to_income": emi_to_income,
            "device_risk": device_risk
        }
    )

    # ---------------- PHASE 1 ----------------
    st.subheader("📊 Composite Credit Score")

    col1, col2, col3 = st.columns(3)
    col1.metric("Bureau Score", result["bureau_score"])
    col2.metric("Internal Score", result["internal_score"])
    col3.metric("Final Score", result["composite_score"])

    band = result["risk_band"]

    st.success(
        f"**Risk Band:** {band['label']}  \n"
        f"**Decision:** {band['decision']}  \n"
        f"**Max Loan Multiple:** {band['max_loan_multiple']}x"
    )

    # ---------------- PHASE 2 ----------------
    st.subheader("🚨 Key Risk Indicators")

    if result["risk_flags"]:
        for f in result["risk_flags"]:
            st.warning(f)
    else:
        st.success("No critical risk flags detected")

    # ---------------- PHASE 3 ----------------
    st.subheader("🧑‍💼 Workflow Ownership")

    if "Auto" in band["decision"]:
        st.info("Handled by **Credit Automation Engine**")
    elif "Manual" in band["decision"]:
        st.info("Assigned to **Credit Analyst Queue**")
    else:
        st.error("Escalated to **Credit Manager**")
