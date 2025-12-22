import streamlit as st
import json
import os
from datetime import datetime


# --- CONFIG LOADER ---
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return {"portal_name": "Dynamic Portal", "urls": []}


def save_config(conf):
    with open("config.json", "w") as f:
        json.dump(conf, f, indent=4)


st.set_page_config(page_title="Backup Manager", layout="wide", page_icon="💾")

st.title("💾 Master Backup & Recovery")
st.write("Apne portal ki saari settings aur API configurations ko yahan se manage karein.")

config = load_config()

# --- TABBED INTERFACE ---
tab1, tab2 = st.tabs(["📤 Backup (Export)", "📥 Restore (Import)"])

with tab1:
    st.subheader("Create a Security Backup")
    st.info(
        "Niche diye gaye button par click karke aap apni saari Saved APIs, AuthKeys aur Settings ka backup le sakte hain.")

    # Prepping JSON for download
    json_string = json.dumps(config, indent=4)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"portal_backup_{timestamp}.json"

    st.download_button(
        label="📥 Download Master Backup File",
        data=json_string,
        file_name=filename,
        mime="application/json",
        use_container_width=True
    )

    st.write("### Backup mein kya-kya save hoga?")
    st.markdown("""
    - Sabhi Registered API URLs
    - Sabhi Encrypted/Plain AuthKeys
    - Custom JSON Request Bodies
    - Portal Preferences (Name, etc.)
    """)

with tab2:
    st.subheader("Restore from Backup")
    st.warning("Savdhaan: Backup file upload karne se aapki current settings overwrite ho jayengi.")

    uploaded_file = st.file_uploader("Apni backup (.json) file yahan upload karein", type=["json"])

    if uploaded_file is not None:
        try:
            # Reading the uploaded JSON
            new_config = json.load(uploaded_file)

            # Basic validation to check if it's a valid portal config
            if "urls" in new_config:
                st.success("✅ Valid Backup File Detected!")
                st.write(f"Sources found: **{len(new_config['urls'])}**")

                if st.button("🚀 Restore Everything Now", use_container_width=True):
                    save_config(new_config)
                    st.balloons()
                    st.success("Settings restored successfully! Portal refresh ho raha hai...")
                    st.rerun()
            else:
                st.error("❌ Invalid Backup File: Is file mein portal ki settings nahi hain.")

        except Exception as e:
            st.error(f"❌ Error loading file: {e}")

# --- RESET OPTION ---
st.divider()
with st.expander("🛑 Factory Reset (Danger Zone)"):
    st.write("Agar aap saari settings delete karke portal ko naya jaisa karna chahte hain, toh niche 'Reset' dabayein.")
    if st.button("Wipe All Data & Settings"):
        empty_config = {"portal_name": "Dynamic Portal", "urls": []}
        save_config(empty_config)
        st.success("System Reset Completed!")
        st.rerun()

# --- SIDEBAR INFO ---
with st.sidebar:
    st.title("System Info")
    st.write(f"Last Backup Check: {datetime.now().strftime('%Y-%m-%d')}")
    st.info("Hamesha nayi API add karne ke baad ek backup download karke rakhein.")