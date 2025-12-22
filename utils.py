def render_common_sidebar():
    """Universal Sidebar: Works with any folder case and path"""
    config = load_config()
    p_name = config.get("portal_name") or "Data Portal"

    with st.sidebar:
        st.title(f"🚀 {p_name}")
        st.divider()

        # Dashboard Link
        st.page_link("Home.py", label="Dashboard", icon="🏠")

        # Pages Links with Error Handling
        # Hum dono options try karenge: 'pages/' aur 'Pages/'
        pages_to_link = [
            {"path": "pages/Ask_Anything.py", "alt": "Pages/Ask_Anything.py", "label": "Ask Anything", "icon": "🔍"},
            {"path": "pages/Quick_Answer.py", "alt": "Pages/Quick_Answer.py", "label": "Quick Answer", "icon": "⚡"},
            {"path": "pages/Settings.py", "alt": "Pages/Settings.py", "label": "Settings", "icon": "⚙️"}
        ]

        for p in pages_to_link:
            try:
                # Try standard small 'pages'
                st.page_link(p["path"], label=p["label"], icon=p["icon"])
            except Exception:
                try:
                    # Try Capital 'Pages' if first one fails
                    st.page_link(p["alt"], label=p["label"], icon=p["icon"])
                except Exception:
                    st.sidebar.warning(f"Could not link {p['label']}")

        st.divider()
        st.caption("Secured AI Engine v2.5")