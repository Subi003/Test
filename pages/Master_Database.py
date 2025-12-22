import streamlit as st
import requests
import json
import os
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


# --- UNIVERSAL DATA FETCHER ---
def fetch_api_data(api_item):
    # Dynamic Headers (Zero Hardcoding)
    headers = {
        "Content-Type": "application/json",
        "AuthKey": api_item.get('auth_key', '')
    }
    body = api_item.get('json_body', {})

    try:
        if api_item['method'] == "POST":
            res = requests.post(api_item['url'], headers=headers, json=body, timeout=15, verify=False)
        else:
            res = requests.get(api_item['url'], headers=headers, timeout=15, verify=False)

        if res.status_code == 200:
            raw_data = res.json()
            # Smart Parser: List dhundne ke liye
            if isinstance(raw_data, list): return raw_data
            if isinstance(raw_data, dict):
                for val in raw_data.values():
                    if isinstance(val, list): return val
            return None
    except:
        return None


# --- UI SETUP ---
st.set_page_config(page_title="Master Database", layout="wide", page_icon="🗂️")

st.title("🗂️ Master Database Viewer")
st.write("Apne sabhi connected sources ka live data yahan dekhein.")

config = load_config()

if not config.get('urls'):
    st.warning("⚠️ Koi API source configure nahi hai. Pehle Settings mein jayein.")
else:
    # --- TOP METRICS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Connected APIs", len(config['urls']))

    # --- API SELECTION ---
    api_labels = [api['label'] for api in config['urls']]
    selected_label = st.selectbox("Select Data Source to View", api_labels)

    # Find selected API details
    selected_api = next(item for item in config['urls'] if item["label"] == selected_label)

    st.divider()

    # --- DATA FETCHING & DISPLAY ---
    with st.spinner(f"Fetching data from {selected_label}..."):
        data = fetch_api_data(selected_api)

        if data:
            df = pd.DataFrame(data)

            # 1. SEARCH BAR FOR TABLE
            search_term = st.text_input(f"🔍 Search within {selected_label}...", "")

            if search_term:
                df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

            # 2. DATA STATS
            st.write(f"Showing **{len(df)}** records from **{selected_label}**")

            # 3. INTERACTIVE TABLE
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={"id": st.column_config.NumberColumn(format="%d")}
            )

            # 4. EXPORT OPTIONS
            st.divider()
            col_a, col_b = st.columns(2)

            # CSV Download
            csv = df.to_csv(index=False).encode('utf-8')
            col_a.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"{selected_label}_export.csv",
                mime='text/csv',
            )

            # JSON Download
            json_str = df.to_json(orient='records', indent=4)
            col_b.download_button(
                label="📦 Download as JSON",
                data=json_str,
                file_name=f"{selected_label}_export.json",
                mime='application/json',
            )

        else:
            st.error(
                f"❌ Data fetch nahi ho paya. Kripya check karein:\n1. URL: `{selected_api['url']}`\n2. AuthKey sahi hai ya nahi.")

# --- SIDEBAR HELP ---
with st.sidebar:
    st.info("💡 **Tip:** Aap table ke columns par click karke data ko sort kar sakte hain.")
    if st.button("🔄 Refresh Master Data"):
        st.rerun()