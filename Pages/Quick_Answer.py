import streamlit as st
import pandas as pd
from utils import fetch_api_data, load_config, render_common_sidebar, dynamic_logic_filter

st.set_page_config(page_title="Quick Answer", layout="centered")
render_common_sidebar()

st.title("⚡ Quick Response")
config = load_config()

user_query = st.text_input("Ask a specific question:")
if user_query and config['urls']:
    # Search across all sources for a quick answer
    for api in config['urls']:
        data = fetch_api_data(api)
        if data:
            df = pd.DataFrame(data)
            res = dynamic_logic_filter(user_query, df)
            if not res.empty:
                st.chat_message("assistant").write(res.iloc[0].to_dict())
                break