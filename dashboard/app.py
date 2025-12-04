import streamlit as st
import json
from pathlib import Path

from scirca.src.serve.monitor import METRICS

st.set_page_config(page_title="SciRCA Monitoring", layout="wide")
st.title("📊 SciRCA Monitoring Dashboard")

st.subheader("Request Stats")
st.metric("Total Requests", METRICS["requests_total"])
st.metric("Total Errors", METRICS["errors_total"])

st.subheader("Latency (ms)")
if METRICS["latency_ms"]:
    st.line_chart(METRICS["latency_ms"])
else:
    st.write("No requests yet.")

st.subheader("Raw Metrics")
st.json(METRICS)
