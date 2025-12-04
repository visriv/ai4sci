import streamlit as st
import subprocess

def render_logs():
    st.subheader("📜 Recent Logs")

    try:
        result = subprocess.check_output(
            "docker logs $(docker ps -q --filter ancestor=scirca-api) --tail 50",
            shell=True, stderr=subprocess.STDOUT
        )
        st.text(result.decode())
    except Exception as e:
        st.error(f"Log read error: {e}")
