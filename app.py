import streamlit as st
import psutil
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="FRAUD DETECTOR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# HEADER
# ==================================================
st.markdown(
    """
    <h1 style="text-align:center;">📊 FRAUD DETECTOR</h1>
    <p style="text-align:center;color:gray;">
    Real-time Monitoring • Federated Intelligence • Explainable AI
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ==================================================
# SYSTEM HEALTH
# ==================================================
st.subheader("🖥️ System Health Overview")

cpu = psutil.cpu_percent(interval=0.1)
ram = psutil.virtual_memory().percent

c1, c2, c3 = st.columns(3)
c1.metric("CPU Usage (%)", cpu)
c2.metric("RAM Usage (%)", ram)
c3.metric("Connected Client Nodes", 3)

# ==================================================
# HARDWARE UTILIZATION CHART
# ==================================================
hardware_df = pd.DataFrame({
    "Component": ["CPU", "RAM"],
    "Usage (%)": [cpu, ram]
})

hardware_fig = px.bar(
    hardware_df,
    x="Component",
    y="Usage (%)",
    color="Component",
    range_y=[0, 100],
    title="Live Infrastructure Utilization"
)

st.plotly_chart(hardware_fig, use_container_width=True)

st.markdown("---")

# ==================================================
# SIDEBAR — RED TEAM ATTACK
# ==================================================
st.sidebar.title("🛑 Red Team Attack Console")
st.sidebar.markdown("Simulate adversarial node behavior")

attack = st.sidebar.button("🚨 Simulate Data Poisoning Attack")

if attack:
    st.sidebar.error("HASH MISMATCH DETECTED")
    st.sidebar.error("NODE QUARANTINED — CLIENT DISCONNECTED")

# ==================================================
# LIVE TRANSACTION SIMULATION
# ==================================================
st.subheader("💹 Incoming Market Transaction")

transaction = {
    "Volume": np.random.randint(800, 2000),
    "Order Frequency": np.random.randint(40, 120),
    "Cancellation Rate (%)": np.random.randint(10, 95),
    "Bid–Ask Spread": round(np.random.uniform(0.5, 6.0), 2)
}

tx_df = pd.DataFrame([transaction])
st.dataframe(tx_df, use_container_width=True)

# ==================================================
# FRAUD RULE ENGINE
# ==================================================
st.subheader("⚠️ Fraud Detection Engine")

fraud_detected = transaction["Cancellation Rate (%)"] > 70

if fraud_detected:
    st.error("🚨 FRAUD DETECTED — Spoofing / Market Manipulation")
else:
    st.success("✅ Transaction Classified as Legitimate")

st.markdown("---")

# ==================================================
# SIMULATED GLOBAL MODEL (FOR STORY)
# ==================================================
st.subheader("🧠 Global Fraud Intelligence Model (Simulated)")

X_train = pd.DataFrame({
    "Volume": np.random.randint(100, 2000, 300),
    "Order Frequency": np.random.randint(10, 120, 300),
    "Cancellation Rate (%)": np.random.randint(0, 100, 300),
    "Bid–Ask Spread": np.random.uniform(0.5, 6.0, 300)
})

y_train = (X_train["Cancellation Rate (%)"] > 70).astype(int)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    random_state=42
)
model.fit(X_train, y_train)

# ==================================================
# EXPLAINABLE AI (SHAP-STYLE VISUAL)
# ==================================================
st.subheader("🔍 Explainable AI — Why Was This Flagged?")

explanation_df = pd.DataFrame({
    "Feature": [
        "Cancellation Rate",
        "Order Frequency",
        "Volume",
        "Bid–Ask Spread"
    ],
    "Impact Score": [
        transaction["Cancellation Rate (%)"] * 0.6,
        transaction["Order Frequency"] * 0.3,
        transaction["Volume"] * 0.05,
        transaction["Bid–Ask Spread"] * 0.05
    ]
})

explanation_fig = px.bar(
    explanation_df,
    x="Impact Score",
    y="Feature",
    orientation="h",
    title="Feature Contribution to Fraud Decision",
    color="Feature"
)

st.plotly_chart(explanation_fig, use_container_width=True)

st.info(
    """
    **Explanation Summary**
    - 🔴 High order cancellation rate is the strongest spoofing signal  
    - 🟠 Elevated order frequency reinforces manipulation behavior  
    - 🟡 Volume and spread provide supporting market context  
    """
)

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.caption(
    "Hackathon Demo • Secure Federated Fraud Detection • Explainable AI Dashboard"
)