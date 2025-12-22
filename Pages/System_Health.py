import streamlit as st
import requests
import json
import os
import time
import pandas as pd
from datetime import datetime


# --- CONFIG LOADER ---
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return {"urls": []}


st.set_page_config(page_title="System Health", layout="wide", page_icon="🛡️")

st.title("🛡️ API Health & Performance Monitor")
st.write("Live status and diagnostic report of all connected data sources.")

config = load_config()

if not config.get('urls'):
    st.info("Checking ke liye koi API source available nahi hai. Settings mein jayein.")
else:
    health_data = []

    st.subheader("Live Status Check")
    progress_bar = st.progress(0)

    for index, api in enumerate(config['urls']):
        start_time = time.time()
        status = "🔴 Offline"
        latency = "N/A"
        records = 0
        last_checked = datetime.now().strftime("%H:%M:%S")

        # Updating progress
        progress_bar.progress((index + 1) / len(config['urls']))

        try:
            # Dynamic Headers & Body
            headers = {
                "Content-Type": "application/json",
                "AuthKey": api.get('auth_key', '')
            }
            body = api.get('json_body', {})

            # API Call
            if api['method'] == "POST":
                res = requests.post(api['url'], headers=headers, json=body, timeout=10, verify=False)
            else:
                res = requests.get(api['url'], headers=headers, timeout=10, verify=False)

            end_time = time.time()
            latency = f"{round((end_time - start_time) * 1000, 2)} ms"

            if res.status_code == 200:
                status = "🟢 Online"
                raw_data = res.json()

                # Dynamic record counting
                if isinstance(raw_data, list):
                    records = len(raw_data)
                elif isinstance(raw_data, dict):
                    for v in raw_data.values():
                        if isinstance(v, list):
                            records = len(v)
                            break
            else:
                status = f"🟠 Error {res.status_code}"

        except Exception as e:
            status = "🔴 Connection Failed"
            latency = "Timeout"

        health_data.append({
            "Source Label": api['label'],
            "Status": status,
            "Latency": latency,
            "Records Found": records,
            "Last Checked": last_checked
        })

    # --- DISPLAY METRICS ---
    df_health = pd.DataFrame(health_data)

    # Grid Layout for Top Indicators
    col1, col2, col3 = st.columns(3)
    active_count = len(df_health[df_health['Status'] == "🟢 Online"])
    col1.metric("Active Sources", f"{active_count}/{len(config['urls'])}")
    col2.metric("Total Records Tracked", df_health['Records Found'].sum())
    col3.metric("Avg Latency",
                f"{round(df_health[df_health['Latency'] != 'Timeout']['Latency'].str.replace(' ms', '').astype(float).mean(), 2)} ms" if active_count > 0 else "N/A")

    st.divider()

    # Master Health Table
    st.dataframe(
        df_health,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn("Status", help="🟢 = Success, 🟠 = API Issue, 🔴 = Server Down"),
            "Latency": st.column_config.TextColumn("Response Time"),
            "Records Found": st.column_config.ProgressColumn("Data Load", min_value=0, max_value=500, format="%d")
        }
    )

    # --- REFRESH BUTTON ---
    if st.button("🔄 Trigger Manual Re-check"):
        st.rerun()

# --- SIDEBAR LOGS ---
with st.sidebar:
    st.success("Monitoring Engine: Active")
    st.write("Yeh page har request par live test karta hai taaki aapko pata rahe ki konsa server down hai.")