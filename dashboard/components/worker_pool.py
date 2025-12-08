import streamlit as st
import requests
import numpy as np

API_BASE = "http://localhost:8000"

def render_worker_pool():
    st.subheader("Autoscaling Worker Pool")

    try:
        resp = requests.get(f"{API_BASE}/worker_pool", timeout=2)
        data = resp.json()
    except Exception as e:
        st.error(f"Failed to fetch worker pool info: {e}")
        return

    workers = data.get("workers", 0)
    backlog = data.get("backlog", 0)
    min_w = data.get("min_workers", 1)
    max_w = data.get("max_workers", 10)

    # Display main stats
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Workers", workers)
    c2.metric("Queue Backlog", backlog)
    c3.metric("Min Workers", min_w)
    c4.metric("Max Workers", max_w)

    # Fetch p95 latency from metrics
    try:
        m = requests.get(f"{API_BASE}/metrics").json()
        lat = m.get("latency_ms", [])
        if len(lat) >= 5:
            p95 = float(np.percentile(lat[-100:], 95))
        else:
            p95 = 0
        st.metric("p95 Latency (ms)", f"{p95:.1f}")
    except:
        st.warning("Could not get p95 latency")
