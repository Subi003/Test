import streamlit as st
from utils import load_config, save_config, render_common_sidebar

st.set_page_config(page_title="Settings", layout="wide")
render_common_sidebar()

st.title("⚙️ System Settings")
config = load_config()

# --- Portal Name Section (One-Time Setup) ---
st.subheader("Global Brand Settings")

# Logic: Agar name pehle se saved hai toh field disable ho jayega
current_name = config.get("portal_name", "")
is_locked = True if current_name != "" else False

col1, col2 = st.columns([3, 1])

with col1:
    new_name = st.text_input(
        "Enter Portal Name:",
        value=current_name,
        disabled=is_locked,
        placeholder="e.g. My Enterprise Data Hub",
        help="Warning: Ek baar save karne ke baad ise change nahi kiya ja sakta."
    )

with col2:
    st.write("##") # Alignment
    if not is_locked:
        if st.button("Save & Lock Name", use_container_width=True):
            if new_name.strip():
                config["portal_name"] = new_name
                save_config(config)
                st.success("Portal Name Locked!")
                st.rerun()
            else:
                st.error("Name khali nahi ho sakta!")
    else:
        st.button("Locked 🔒", disabled=True, use_container_width=True)

st.divider()

# --- Master Key Section ---
st.subheader("API Security")
master_key = st.text_input("Master Auth Key:", value=config.get("master_auth_key", ""), type="password")
if st.button("Update Master Key"):
    config["master_auth_key"] = master_key
    save_config(config)
    st.success("Master Key has been updated securely.")

# --- API Sources Section ---
st.subheader("Data Sources (APIs)")
# Yahan aap apna purana URL add karne wala logic continue rakh sakte hain
st.info("Additional API configuration can be added here.")