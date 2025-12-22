import streamlit as st
import json
import os
import requests
import pandas as pd
import re


# --- CONFIGURATION MANAGER ---
def load_config():
    """Server-safe config loader (Fixes KeyError)"""
    default_config = {
        "portal_name": "",
        "master_auth_key": "",
        "urls": []
    }
    if not os.path.exists("config.json"):
        return default_config
    try:
        with open("config.json", "r") as f:
            user_config = json.load(f)
            for key in default_config:
                if key in user_config:
                    default_config[key] = user_config[key]
            return default_config
    except:
        return default_config


def save_config(conf):
    """Config file save karne ke liye"""
    with open("config.json", "w") as f:
        json.dump(conf, f, indent=4)


# --- CENTRAL DYNAMIC FILTER ENGINE ---
def dynamic_logic_filter(query, df):
    """Dynamic Search logic for Numeric and Text queries"""
    query = query.lower().strip()
    if not query: return df

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


# --- SECURE API FETCHER ---
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
    """Navigation UI"""
    config = load_config()
    p_name = config.get("portal_name") or "Data Portal"
    with st.sidebar:
        st.title(f"🚀 {p_name}")
        st.divider()
        st.page_link("Home.py", label="Dashboard", icon="🏠")
        st.page_link("pages/Ask_Anything.py", label="Ask Anything", icon="🔍")
        st.page_link("pages/Quick_Answer.py", label="Quick Answer", icon="⚡")
        st.page_link("pages/Settings.py", label="Settings", icon="⚙️")