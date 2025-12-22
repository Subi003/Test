import streamlit as st
import pandas as pd
from utils import load_config, fetch_api_data, render_common_sidebar

st.set_page_config(page_title="Dashboard", layout="wide")
render_common_sidebar()

config = load_config()
st.title(f"🏢 {config.get('portal_name') or 'Intelligence Portal'}")
st.write(f"System Status: **Active** | 🕒 {pd.Timestamp.now().strftime('%d-%m-%Y')}")

if not config.get('urls'):
    st.info("No API sources configured. Please go to Settings to add data sources.")
else:
    # Metrics
    st.subheader("Live Metrics")
    cols = st.columns(len(config['urls']) if len(config['urls']) < 4 else 4)
    datasets = {}
    for i, api in enumerate(config['urls']):
        data = fetch_api_data(api)
        if data:
            df = pd.DataFrame(data)
            datasets[api['label']] = df
            with cols[i % 4]:
                with st.container(border=True):
                    st.metric(api['label'], f"{len(df)} Records")
        else:
            datasets[api['label']] = None

    st.divider()
    # Data View
    st.subheader("📊 Data Exploration")
    tabs = st.tabs([api['label'] for api in config['urls']])
    for i, api in enumerate(config['urls']):
        with tabs[i]:
            df_res = datasets.get(api['label'])
            if df_res is not None:
                st.dataframe(df_res, use_container_width=True, hide_index=True)
            else:
                st.error("Connection Failed")