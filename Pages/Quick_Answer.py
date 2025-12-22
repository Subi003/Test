import streamlit as st
import pandas as pd
from utils import fetch_api_data, load_config, render_common_sidebar, dynamic_logic_filter

st.set_page_config(page_title="Quick Answer", layout="centered")
render_common_sidebar()

st.title("⚡ Quick AI Answer")
config = load_config()

st.write("Ask a specific question like *'which item has price 200?'*")

user_query = st.text_input("Enter your question:")

if user_query and config.get('urls'):
    found = False
    # Searching across ALL configured APIs
    for api in config['urls']:
        data = fetch_api_data(api)
        if data:
            df = pd.DataFrame(data)
            result_df = dynamic_logic_filter(user_query, df)

            if not result_df.empty:
                st.success(f"Found in source: **{api['label']}**")
                top_result = result_df.iloc[0]  # Taking the best match

                with st.chat_message("assistant"):
                    st.write("Based on your query, here is the best match:")
                    st.json(top_result.to_dict())
                found = True
                break

    if not found:
        st.error("Sorry, I couldn't find a direct match for that query.")
elif not config.get('urls'):
    st.info("Please add data sources in Settings first.")