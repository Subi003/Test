import streamlit as st
import json
import os
import requests
import pandas as pd
import re


# --- CONFIGURATION MANAGER ---
def load_config():
    default_config = {
        "portal_name": "",
        "master_auth_key": "",
        "urls": []
    }
    # Streamlit Cloud par path issues se bachne ke liye absolute path
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, "config.json")

    if not os.path.exists(config_path):
        return default_config
    try:
        with open(config_path, "r") as f:
            user_config = json.load(f)
            for key in default_config:
                if key in user_config:
                    default_config[key] = user_config[key]
            return default_config
    except:
        return default_config


def save_config(conf):
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, "config.json")
    with open(config_path, "w") as f:
        json.dump(conf, f, indent=4)


def dynamic_logic_filter(query, df):
    query = query.lower().strip()
    if not query or df is None or df.empty: return df

    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", query)

    if numbers:
        target_val = float(numbers[0])
        target_col = next((c for c in num_cols if c.lower() in query), None)
        if not target_col and num_cols: target_col = num_cols[0]

        ops = {
            'gt': ['jyada', 'upar', 'above', 'more', 'high', '>', 'greater'],
            'lt': ['kam', 'niche', 'below', 'less', 'low', '<', 'under'],
            'eq': ['barabar', 'equal', 'exact', '==', 'hai']
        }
        if target_col:
            if any(w in query for w in ops['gt']): return df[df[target_col] > target_val]
            if any(w in query for w in ops['lt']): return df[df[target_col] < target_val]
            if any(w in query for w in ops['eq']): return df[df[target_col] == target_val]

    mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
    return df[mask]


@st.cache_data(ttl=300, show_spinner=False)
def fetch_api_data(api_item):
    config = load_config()
    api_key = api_item.get('auth_key') or config.get('master_auth_key', '')
    headers = {"Content-Type": "application/json", "AuthKey": api_key}
    try:
        res = requests.get(api_item['url'], headers=headers, timeout=7, verify=False)
        if res.status_code == 200:
            raw = res.json()
            if isinstance(raw, list): return raw
            if isinstance(raw, dict):
                for v in raw.values():
                    if isinstance(v, list): return v
                return [raw]
    except:
        return None
    return None


def render_common_sidebar():
    config = load_config()
    p_name = config.get("portal_name") or "Data Portal"

    with st.sidebar:
        st.title(f"🚀 {p_name}")
        st.divider()

        # Link to Home
        st.page_link("Home.py", label="Dashboard", icon="🏠")

        # Pages folder checks
        potential_pages = [
            ("pages/Ask_Anything.py", "Ask Anything", "🔍"),
            ("pages/Quick_Answer.py", "Quick Answer", "⚡"),
            ("pages/Settings.py", "Settings", "⚙️")
        ]

        for path, label, icon in potential_pages:
            if os.path.exists(path):
                st.page_link(path, label=label, icon=icon)
            elif os.path.exists(path.replace("pages/", "Pages/")):
                st.page_link(path.replace("pages/", "Pages/"), label=label, icon=icon)
            else:
                st.caption(f"⚠️ {label} not found")

        st.divider()
        st.caption("Secured AI Engine v2.5")