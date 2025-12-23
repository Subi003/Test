import streamlit as st
import json
from utils import load_config, save_config, render_common_sidebar

st.set_page_config(page_title="Settings", layout="wide")
render_common_sidebar()

st.title("⚙️ System Configuration")
config = load_config()

# 1. Portal Branding Section
st.subheader("🏢 Branding")
current_name = config.get("portal_name", "")
# Agar name pehle se set hai toh lock rahega (jaisa aapne manga tha)
is_locked = True if current_name != "" else False

new_name = st.text_input("Set Portal Name:", value=current_name, disabled=is_locked)

if not is_locked:
    if st.button("Save & Lock Name"):
        if new_name.strip():
            config["portal_name"] = new_name
            save_config(config)
            st.success("Portal Name Locked!")
            st.rerun()

st.divider()

# 2. API Sources Section (The JSON/List Field)
st.subheader("🔗 Data Sources (API URLs)")
st.write("Apne API endpoints yahan JSON format mein manage karein.")

# Current URLs ko text area mein dikhana
current_urls = config.get("urls", [])
urls_json_str = json.dumps(current_urls, indent=4)

updated_urls_str = st.text_area(
    "Edit API Configuration (JSON):",
    value=urls_json_str,
    height=250,
    help="Format: [{'label': 'Source Name', 'url': 'https://api.example.com', 'auth_key': 'optional'}]"
)

# 3. Master Auth Key
st.subheader("🔑 Security")
m_key = st.text_input("Master Auth Key:", value=config.get("master_auth_key", ""), type="password")

# --- SAVE ALL BUTTON ---
if st.button("Save All Settings", type="primary"):
    try:
        # JSON string ko vapas list mein convert karna
        new_urls_list = json.loads(updated_urls_str)

        # Validation
        if not isinstance(new_urls_list, list):
            st.error("Error: API Sources must be a List [ ].")
        else:
            config["urls"] = new_urls_list
            config["master_auth_key"] = m_key
            save_config(config)
            st.success("✅ Settings updated successfully!")
            st.rerun()
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format! Please check brackets and commas.")

# Help Section
with st.expander("💡 Help: JSON Example"):
    st.code("""
[
    {
        "label": "Store Data",
        "url": "https://fakestoreapi.com/products",
        "auth_key": ""
    },
    {
        "label": "User Data",
        "url": "https://jsonplaceholder.typicode.com/users"
    }
]
    """, language="json")