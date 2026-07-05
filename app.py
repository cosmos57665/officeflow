"""OfficeFlow — Streamlit entry point: branding, navigation, module routing."""
import streamlit as st

from modules import ask, docs, inbox, minutes

st.set_page_config(page_title="OfficeFlow", layout="wide")

MODULES = {
    "Minutes": minutes,
    "Inbox": inbox,
    "Docs": docs,
    "Ask": ask,
}

with st.sidebar:
    st.title("OfficeFlow")
    st.caption("AI Office Automation Suite")
    choice = st.radio("Navigation", list(MODULES.keys()))
    st.toggle("Demo Mode", key="demo_mode")

MODULES[choice].render()

st.divider()
st.caption("Built with Python · Whisper · Claude API")
