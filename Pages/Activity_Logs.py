import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime


# --- CONFIG & LOG HELPERS ---
def load_logs():
    if os.path.exists("activity_logs.json"):
        with open("activity_logs.json", "r") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, list) else []
            except:
                return []
    return []


def clear_logs():
    if os.path.exists("activity_logs.json"):
        os.remove("activity_logs.json")


# --- UI SETUP ---
st.set_page_config(page_title="System Logs", layout="wide")
st.title("📜 System Activity & Audit Logs")
st.markdown("Yeh page aapke portal par hone wali har activity ko track karta hai.")

# --- LOAD DATA ---
logs = load_logs()

if logs:
    df = pd.DataFrame(logs)

    # 1. METRICS SECTION
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Activities", len(df))
    col2.metric("Latest Action", df.iloc[-1]['action'])
    col3.metric("Last Active", df.iloc[-1]['timestamp'].split(" ")[1])

    st.divider()

    # 2. FILTERS & SEARCH
    c1, c2 = st.columns([2, 1])
    with c1:
        search_log = st.text_input("Search in Logs", placeholder="e.g. Sudhanshu ya API_TEST")
    with c2:
        filter_action = st.multiselect("Filter by Category",
                                       options=df['action'].unique(),
                                       default=df['action'].unique())

    # Filtering Logic
    filtered_df = df[df['action'].isin(filter_action)]
    if search_log:
        filtered_df = filtered_df[
            filtered_df.astype(str).apply(lambda x: x.str.contains(search_log, case=False)).any(axis=1)]

    # 3. LOG TABLE DISPLAY
    st.subheader("Activity History")
    # Latest logs on top
    st.dataframe(filtered_df.iloc[::-1], use_container_width=True)

    # 4. ACTIONS (Export & Clear)
    st.divider()
    ca, cb = st.columns([1, 1])

    with ca:
        # Export to CSV
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Log Report (CSV)", csv, "system_logs.csv", "text/csv")

    with cb:
        if st.button("🗑️ Reset/Clear All Logs", type="secondary", use_container_width=True):
            clear_logs()
            st.success("Logs cleared successfully!")
            st.rerun()

else:
    st.info(
        "Abhi tak koi activity record nahi hui hai. Jaise hi aap API test karenge ya data search karenge, logs yahan dikhai denge.")

# --- SIDEBAR NAV ---
with st.sidebar:
    st.page_link("Home.py", label="Dashboard", icon="🏠")
    st.page_link("pages/Ask_Anything.py", label="Search Data", icon="🔍")
    st.page_link("pages/Settings.py", label="Settings", icon="⚙️")