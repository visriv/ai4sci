import streamlit as st
import requests
import json

def render_test_inference():
    st.subheader("⚡ Quick RCA Test")

    run_summary = st.text_area("Run Summary")
    logs = st.text_area("Logs (one per line)")
    model_tag = st.text_input("Model Tag", "rca-v2")

    if st.button("Run RCA"):
        payload = {
            "run_summary": run_summary,
            "logs": [l for l in logs.split("\n") if l],
            "metrics": {},
            "model_tag": model_tag
        }

        with st.spinner("Running analysis..."):
            try:
                res = requests.post(
                    "http://localhost:8000/rca",
                    json=payload,
                    timeout=120
                )
                st.json(res.json())
            except Exception as e:
                st.error(str(e))
