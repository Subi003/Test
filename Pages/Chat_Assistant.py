import streamlit as st
import requests
import json
import os
import pandas as pd
import difflib


def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    return {"urls": []}


def fetch_api_data(api_item):
    # Dynamic Headers - No hardcoded keys here
    headers = {
        "Content-Type": "application/json",
        "AuthKey": api_item.get('auth_key', '')
    }
    try:
        if api_item['method'] == "POST":
            res = requests.post(api_item['url'], headers=headers, timeout=15, verify=False)
        else:
            res = requests.get(api_item['url'], headers=headers, timeout=15, verify=False)

        if res.status_code == 200:
            raw_data = res.json()
            # Automatic List Discovery (Dynamic Parsing)
            if isinstance(raw_data, list): return raw_data
            if isinstance(raw_data, dict):
                for val in raw_data.values():
                    if isinstance(val, list): return val
        return None
    except:
        return None


st.set_page_config(page_title="AI Chat", layout="wide", page_icon="🤖")
st.title("🤖 Intelligent Assistant")

config = load_config()

if not config['urls']:
    st.warning("Pehle Settings mein API add karein.")
else:
    # Sidebar Source Selection
    api_map = {a['label']: a for a in config['urls']}
    selection = st.sidebar.selectbox("Select Data Source", list(api_map.keys()))
    selected_api = api_map[selection]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Ask me something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Analyzing Source..."):
            data = fetch_api_data(selected_api)

            if data:
                df = pd.DataFrame(data)
                cols = df.columns.tolist()
                words = prompt.lower().split()

                # 1. Row Matching Logic
                found_row = None
                for w in words:
                    if len(w) < 3: continue
                    mask = df.apply(lambda r: r.astype(str).str.contains(w, case=False, na=False).any(), axis=1)
                    if not df[mask].empty:
                        found_row = df[mask].iloc[0]
                        break

                # 2. Column Matching Logic (Fuzzy)
                if found_row is not None:
                    best_col = None
                    for w in words:
                        matches = difflib.get_close_matches(w, cols, n=1, cutoff=0.5)
                        if matches:
                            best_col = matches[0]
                            break

                    if best_col:
                        response = f"**{best_col}** for this record is: `{found_row[best_col]}`"
                    else:
                        response = "Record mil gaya hai. Niche details dekhein:"
                        st.json(found_row.to_dict())
                else:
                    response = "Maaf kijiye, mujhe is source mein koi matching record nahi mila."
            else:
                response = "❌ API se data fetch nahi ho paya. AuthKey ya URL check karein."

        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})