import streamlit as st
import pandas as pd
import plotly.express as px
from utils import fetch_api_data, load_config, render_common_sidebar

# Page Configuration
st.set_page_config(page_title="Analytics Dashboard", layout="wide")
render_common_sidebar()

st.title("📊 Data Analytics Dashboard")
config = load_config()

if not config['urls']:
    st.warning("No data sources found. Please add an API in Settings.")
else:
    # 1. Source Selection
    selected_label = st.selectbox("📁 Select Data Source", [a['label'] for a in config['urls']])
    selected_api = next(a for a in config['urls'] if a['label'] == selected_label)

    data = fetch_api_data(selected_api)

    if data:
        df = pd.DataFrame(data)

        # Numerical aur Categorical columns alag karna
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        obj_cols = df.select_dtypes(include=['object']).columns.tolist()

        if not num_cols:
            st.error("Is dataset mein numerical columns (numbers) nahi hain, isliye analytics nahi dikhaya ja sakta.")
        else:
            st.divider()

            # 2. RADIO BUTTON FOR CHART SELECTION
            # Horizontal layout se ye ek modern navigation bar jaisa dikhega
            chart_type = st.radio(
                "📈 Choose Visualization Type:",
                ["Bar Chart", "Line Chart", "Area Chart", "Scatter Plot", "Pie Chart", "Box Plot"],
                horizontal=True
            )

            st.divider()

            # 3. AXIS SELECTION
            c1, c2 = st.columns(2)
            with c1:
                x_axis = st.selectbox("Select X-Axis (Categories)", obj_cols if obj_cols else df.columns)
            with c2:
                y_axis = st.selectbox("Select Y-Axis (Values)", num_cols)

            # 4. CHART GENERATION LOGIC
            fig = None

            if chart_type == "Bar Chart":
                fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, text_auto='.2s',
                             title=f"Comparison of {y_axis} across {x_axis}")

            elif chart_type == "Line Chart":
                fig = px.line(df, x=x_axis, y=y_axis, markers=True,
                              title=f"Trend Analysis: {y_axis} vs {x_axis}")

            elif chart_type == "Area Chart":
                fig = px.area(df, x=x_axis, y=y_axis,
                              title=f"Cumulative Growth: {y_axis}")

            elif chart_type == "Scatter Plot":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, size=y_axis,
                                 title=f"Correlation between {x_axis} and {y_axis}")

            elif chart_type == "Pie Chart":
                fig = px.pie(df, names=x_axis, values=y_axis, hole=0.4,
                             title=f"Percentage Share of {y_axis}")

            elif chart_type == "Box Plot":
                fig = px.box(df, x=x_axis, y=y_axis, color=x_axis,
                             title=f"Statistical Distribution of {y_axis}")

            # 5. DISPLAY CHART
            if fig:
                st.plotly_chart(fig, use_container_width=True)

            # 6. RAW DATA SUMMARY
            with st.expander("📝 View Detailed Statistics"):
                st.write(df.describe())
                st.dataframe(df, use_container_width=True)
    else:
        st.error("API se data fetch nahi ho saka. Connection check karein.")