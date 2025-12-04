import streamlit as st
from src.serve.monitor import METRICS

def render_metrics():
    st.subheader("📊 Runtime Metrics")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Requests", METRICS["requests_total"])
    with col2:
        st.metric("Total Errors", METRICS["errors_total"])

    st.markdown("### 🔵 Latency (ms)")
    if METRICS["latency_ms"]:
        st.line_chart(METRICS["latency_ms"])
    else:
        st.info("No latency data yet — send a request!")
