import streamlit as st

# --- UI SETUP ---
st.set_page_config(page_title="System Documentation", layout="wide")

st.title("📖 Documentation & User Guide")
st.markdown("Yeh guide aapko portal ke saare features aur unhe use karne ka sahi tarika batayegi.")

# --- SECTION 1: GETTING STARTED ---
st.divider()
st.header("🚀 Quick Start Guide")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 1: API Configuration")
    st.write("""
    1. **Settings** page par jayein.
    2. **Add New API** form bharein.
    3. **AuthKey** field mein apni key daalein.
    4. Save karne ke baad **Test** button se check karein ki connection green hai ya nahi.
    """)

with col2:
    st.subheader("Step 2: Searching Data")
    st.write("""
    1. **Ask Anything** page par jayein.
    2. Dropdown se apni API select karein.
    3. Data table format mein niche aa jayega.
    """)

# --- SECTION 3: CHAT ASSISTANT LOGIC ---
st.divider()
st.header("🤖 AI Chat Assistant (Smart Search)")
st.info("Chat Assistant kisi bhi API ke columns ko apne aap (Dynamically) samajh leta hai.")

st.markdown("""
- **Point-to-Point Jawab:** Agar aap puchenge *"user ka mobile kya hai?"*, toh wo sirf mobile number dikhayega.
- **Natural Language:** Aap Hindi aur English mix karke puch sakte hain.
- **Multi-API Support:** Sidebar se API change karke aap alag-alag departments ke sawal puch sakte hain.
""")

# --- SECTION 4: SYSTEM HEALTH & MONITORING ---
st.divider()
st.header("🛡️ Monitoring & Logs")
c1, c2 = st.columns(2)

with c1:
    st.subheader("System Health")
    st.write("Is page par aap live dekh sakte hain ki kaunsi API online hai aur uski speed (ms) kitni hai.")

with c2:
    st.subheader("Activity Logs")
    st.write("Yahan har search aur edit ka record rehta hai, jise aap audit ke liye CSV mein download kar sakte hain.")

# --- SECTION 5: BACKUP & SECURITY ---
st.divider()
st.header("💾 Backup & Security")
with st.expander("System Backup kaise lein?"):
    st.write("""
    1. **Backup Manager** page par jayein.
    2. **Download Backup** button par click karein.
    3. Ek `.json` file save ho jayegi jisme aapki sari settings hongi.
    4. Kisi bhi naye system par is file ko **Upload** karke apna pura portal 1 minute mein restore kar sakte hain.
    """)

# --- FOOTER ---
st.sidebar.success("v2.0 - Autonomous Portal")
st.sidebar.info("Authorized Access Only")

with st.sidebar:
    st.page_link("Home.py", label="Home Dashboard", icon="🏠")
    st.page_link("pages/Ask_Anything.py", label="Search Data", icon="🔍")
    st.page_link("pages/Chat_Assistant.py", label="AI Chat", icon="🤖")
    st.page_link("pages/Settings.py", label="Settings", icon="⚙️")