import streamlit as st
import json
from pathlib import Path

REGISTRY = Path("registry")

def render_model_registry():
    st.subheader("🤖 Model Registry")

    if not REGISTRY.exists():
        st.info("Registry folder not found.")
        return

    for f in REGISTRY.glob("*.json"):
        cfg = json.loads(f.read_text())
        st.json({f.name: cfg})
