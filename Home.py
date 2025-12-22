import streamlit as st
import pandas as pd
from utils import load_config, fetch_api_data, render_common_sidebar

# 1. Page Configuration
st.set_page_config(page_title="Data Dashboard", layout="wide", page_icon="🏢")
render_common_sidebar()

# 2. Configuration Load
config = load_config()
portal_title = config.get('portal_name') if config.get('portal_name') else "Data Intelligence Portal"

st.title(f"🏢 {portal_title}")
st.write(f"System Status: **Active** | 🕒 {pd.Timestamp.now().strftime('%d-%m-%Y %H:%M')}")

st.divider()

if not config.get('urls'):
    st.info("💡 Welcome! Please go to **Settings** to configure your API data sources.")
else:
    # 3. Summary Metrics Section
    st.subheader("Live Data Metrics")

    num_sources = len(config['urls'])
    grid_cols = st.columns(num_sources if num_sources < 4 else 4)

    fetched_datasets = {}

    for i, api in enumerate(config['urls']):
        data = fetch_api_data(api)
        col_idx = i % 4

        if data:
            df = pd.DataFrame(data)
            fetched_datasets[api['label']] = df

            with grid_cols[col_idx]:
                with st.container(border=True):
                    # Metric hamesha poore data ka count dikhayega
                    st.metric(label=api['label'], value=f"{len(df)} Records")
                    st.caption("✅ Connected")
        else:
            fetched_datasets[api['label']] = None
            with grid_cols[col_idx]:
                with st.container(border=True):
                    st.metric(label=api['label'], value="Error")
                    st.error("Connection Failed")

    st.divider()

    # 4. Data Preview Section (Tabs)
    st.subheader("📊 Data Exploration")
    tabs = st.tabs([api['label'] for api in config['urls']])

    for i, api in enumerate(config['urls']):
        with tabs[i]:
            df_result = fetched_datasets.get(api['label'])
            if df_result is not None:
                # --- FIX: head(10) ko hata kar poora data ya badi limit set karna ---
                # Agar poora data dikhana hai toh sirf 'df_result' likhein
                # Performance ke liye hum head(100) use kar rahe hain
                st.dataframe(df_result, use_container_width=True, hide_index=True)
                st.caption(f"Showing all {len(df_result)} records from {api['label']}")
            else:
                st.error(f"Source '{api['label']}' ka data load nahi ho saka.")

# Sidebar Branding
st.sidebar.markdown("---")
st.sidebar.caption("Secured Enterprise Engine v2.5")