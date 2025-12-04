import streamlit as st

from components.metrics import render_metrics
from components.logs import render_logs
from components.model_registry import render_model_registry
from components.test_inference import render_test_inference

st.set_page_config(page_title="SciRCA Dashboard", layout="wide")

st.title("🧠 SciRCA Monitoring & Ops Dashboard")
st.markdown("Real-time monitoring • Model registry • Canary eval • Test interface")

tabs = st.tabs(["📊 Metrics", "📜 Logs", "🤖 Model Registry", "🧪 Test RCA"])

with tabs[0]:
    render_metrics()

with tabs[1]:
    render_logs()

with tabs[2]:
    render_model_registry()

with tabs[3]:
    render_test_inference()
