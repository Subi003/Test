import streamlit as st
import pandas as pd
import plotly.express as px  # requirements.txt mein plotly zaroor add karein
from utils import load_config, fetch_api_data, render_common_sidebar

# 1. Page Config
st.set_page_config(page_title="Data Analytics", layout="wide", page_icon="📈")
render_common_sidebar()

st.title("📈 Data Analytics & Insights")

config = load_config()

if not config.get('urls'):
    st.info("Please configure API sources in Settings to see analytics.")
else:
    # 2. Source Selection
    labels = [api['label'] for api in config['urls']]
    selected_source = st.selectbox("Select Data Source for Analysis:", labels)

    api_info = next(api for api in config['urls'] if api['label'] == selected_source)

    # 3. Data Fetching with Error Handling
    with st.spinner("Analyzing data..."):
        data = fetch_api_data(api_info)

    if data:
        df = pd.DataFrame(data)

        if not df.empty:
            # --- Summary Cards ---
            st.subheader(f"Summary: {selected_source}")
            m1, m2, m3 = st.columns(3)

            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

            m1.metric("Total Records", len(df))

            if num_cols:
                m2.metric("Avg " + num_cols[0], round(df[num_cols[0]].mean(), 2))
                m3.metric("Max " + num_cols[0], df[num_cols[0]].max())
            else:
                m2.metric("Numeric Columns", "None Found")
                m3.metric("Status", "Categorical Data")

            st.divider()

            # --- Visualizations ---
            col_a, col_b = st.columns(2)

            with col_a:
                st.write("### Data Distribution")
                if num_cols:
                    fig1 = px.histogram(df, x=num_cols[0], title=f"Distribution of {num_cols[0]}",
                                        color_discrete_sequence=['#00CC96'])
                    st.plotly_chart(fig1, use_container_width=True)
                else:
                    st.info("No numeric data for histogram.")

            with col_b:
                st.write("### Category Breakdown")
                if cat_cols:
                    # Pehla categorical column pick karke uska count dikhana
                    top_cat = cat_cols[0]
                    cat_counts = df[top_cat].value_counts().reset_index()
                    fig2 = px.pie(cat_counts, values='count', names=top_cat, title=f"Top Categories in {top_cat}")
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No categorical data for pie chart.")

        else:
            st.warning("The API returned an empty dataset. Nothing to analyze.")
    else:
        st.error("Failed to fetch data from the API. Check your connection or AuthKey.")

# Branding
st.sidebar.markdown("---")
st.sidebar.caption("Analytics Engine v1.2")