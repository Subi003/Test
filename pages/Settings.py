import streamlit as st
from utils import load_config, save_config, render_common_sidebar

st.set_page_config(page_title="Settings", layout="wide")
render_common_sidebar()

st.title("⚙️ System Settings")
config = load_config()

# Portal Name Lock Logic
current_name = config.get("portal_name", "")
is_locked = True if current_name != "" else False

st.subheader("General Branding")
new_name = st.text_input("Set Portal Name (One-time):", value=current_name, disabled=is_locked)

if not is_locked:
    if st.button("Save & Lock Portal Name"):
        if new_name.strip():
            config["portal_name"] = new_name
            save_config(config)
            st.success("Portal Name Saved!")
            st.rerun()

st.divider()
# API Config
st.subheader("Security & Sources")
m_key = st.text_input("Master Auth Key:", value=config.get("master_auth_key", ""), type="password")
if st.button("Update Master Key"):
    config["master_auth_key"] = m_key
    save_config(config)
    st.success("Updated!")