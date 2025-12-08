import streamlit as st
import requests

API_URL = "http://localhost:8000/metrics"

def fetch_metrics():
    """Fetch metrics from Docker FastAPI."""
    try:
        res = requests.get(API_URL, timeout=2)
        if res.status_code == 200:
            return res.json()
        return {"requests_total": 0, "errors_total": 0, "latency_ms": []}
    except Exception:
        return {"requests_total": 0, "errors_total": 0, "latency_ms": []}

def render_metrics():
    st.subheader("📊 Runtime Metrics")

    metrics = fetch_metrics()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Requests", metrics.get("requests_total", 0))
    with col2:
        st.metric("Total Errors", metrics.get("errors_total", 0))

    st.markdown("### 🔵 Latency (ms)")

    latency_list = metrics.get("latency_ms", [])

    if latency_list:
        st.line_chart(latency_list)
    else:
        st.info("No latency data yet — send a request!")
