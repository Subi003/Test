import streamlit as st
import pandas as pd
from utils import fetch_api_data, load_config, render_common_sidebar, dynamic_logic_filter

st.set_page_config(page_title="Ask Anything", layout="wide")
render_common_sidebar()

st.title("🔍 Universal AI Search")
config = load_config()

if config['urls']:
    c1, c2 = st.columns([2, 1])
    selected_label = c1.selectbox("Source:", [a['label'] for a in config['urls']])
    view_mode = c2.radio("Format:", ["📊 Table", "🖼️ Card View"], horizontal=True)

    api = next(a for a in config['urls'] if a['label'] == selected_label)
    user_query = st.text_input("What are you looking for?", placeholder="e.g. rating 2.2 se jyada")

    if user_query:
        data = fetch_api_data(api)
        if data:
            df = pd.DataFrame(data)
            final_df = dynamic_logic_filter(user_query, df)

            if not final_df.empty:
                if view_mode == "📊 Table":
                    st.dataframe(final_df, use_container_width=True, hide_index=True)
                else:
                    for _, row in final_df.iterrows():
                        with st.container(border=True):
                            col_img, col_txt = st.columns([1, 4])
                            # Image Logic
                            img_url = next((row[c] for c in df.columns if any(k in c.lower() for k in ['image', 'url', 'pic']) and str(row[c]).startswith('http')), None)
                            with col_img:
                                if img_url: st.image(img_url, use_container_width=True)
                                else: st.write("📷 No Image")
                            with col_txt:
                                st.subheader(row.iloc[0])
                                st.write(row.to_dict())
            else:
                st.warning("No matches found.")