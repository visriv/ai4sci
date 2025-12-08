import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"

def render_autoscaling_charts():
    st.subheader("Autoscaling Time-Series")

    try:
        m = requests.get(f"{API}/metrics").json()
    except:
        st.error("Could not fetch metrics")
        return

    hist = m["history"]
    if len(hist["timestamp"]) < 2:
        st.info("Waiting for more data…")
        return

    df = pd.DataFrame({
        "time": hist["timestamp"],
        "workers": hist["workers"],
        "backlog": hist["backlog"],
        "p95_latency": hist["p95_latency"],
    })
    df["time"] = pd.to_datetime(df["time"], unit='s')

    st.line_chart(df.set_index("time")[["workers", "backlog"]])
    st.line_chart(df.set_index("time")[["p95_latency"]])
