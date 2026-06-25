import streamlit as st
from datetime import datetime
import requests

st.set_page_config(
    page_title="Bharath Climate Twin — FENRIR",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Hide sidebar completely ───────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

.stApp {
    background: #0a1628 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.main .block-container {
    padding: 70px 2rem 2rem !important;
    max-width: 1400px !important;
}

/* Nav buttons override */
.nav-btn > button {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 6px !important;
    color: #9ec4d4 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.72em !important;
    font-weight: 500 !important;
    letter-spacing: 0.8px !important;
    padding: 5px 12px !important;
    transition: all 0.2s !important;
    white-space: nowrap !important;
}
.nav-btn > button:hover {
    background: rgba(72,202,228,0.1) !important;
    border-color: rgba(72,202,228,0.25) !important;
    color: #48cae4 !important;
}
.nav-btn-active > button {
    background: rgba(72,202,228,0.12) !important;
    border-color: rgba(72,202,228,0.35) !important;
    color: #48cae4 !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a1628; }
::-webkit-scrollbar-thumb { background: #1e6091; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Session state for page ────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Mission Control"

# ── TOP NAVBAR ────────────────────────────────────────────
now = datetime.now()

nav_pages = [
    ("🌐", "Mission Control"),
    ("🔥", "Heat-Seeking"),
    ("🌧️", "Rain Predict"),
    ("🌿", "Forest"),
    ("💧", "Underground"),
    ("🤖", "AI Assistant"),
    ("✅", "Validation"),
]

# Fixed top bar
st.markdown(f"""
<div style="position:fixed;top:0;left:0;right:0;z-index:9999;
            background:linear-gradient(90deg,#061020 0%,#0a1a30 50%,#061020 100%);
            border-bottom:1px solid rgba(72,202,228,0.15);
            padding:6px 20px;display:flex;align-items:center;gap:0;
            backdrop-filter:blur(10px);">
  <div style="font-family:'Syne',sans-serif;font-size:1em;font-weight:800;
              letter-spacing:4px;color:#48cae4;margin-right:24px;
              text-shadow:0 0 15px rgba(72,202,228,0.3);white-space:nowrap;">
    🌧️ FENRIR
  </div>
  <div id="nav-placeholder" style="flex:1;"></div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:0.68em;
              color:#5a8a9f;white-space:nowrap;margin-left:16px;">
    📅 {now.strftime('%d %b %Y')} &nbsp;|&nbsp; 🕐 {now.strftime('%H:%M')} IST
  </div>
</div>
""", unsafe_allow_html=True)

# Nav buttons using Streamlit columns (these actually work!)
nav_col_brand, *nav_cols, nav_col_time = st.columns(
    [1.2] + [1]*7 + [1.5]
)

# Brand (empty — handled by HTML above)
nav_col_brand.markdown("")
nav_col_time.markdown("")

for col, (icon, page_name) in zip(nav_cols, nav_pages):
    is_active = st.session_state.page == page_name
    css_class = "nav-btn-active" if is_active else "nav-btn"
    with col:
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if st.button(f"{icon} {page_name}", key=f"nav_{page_name}",
                     use_container_width=True):
            st.session_state.page = page_name
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── LOAD CSS ──────────────────────────────────────────────
def load_css():
    import os
    css_paths = ["assets/styles.css", "styles.css"]
    for path in css_paths:
        if os.path.exists(path):
            with open(path) as f:
                st.markdown(f"<style>{f.read()}</style>",
                            unsafe_allow_html=True)
            return
load_css()

# ── ROUTE TO PAGE ─────────────────────────────────────────
page = st.session_state.page

if page == "Mission Control":
    from pages.mission_control import show
    show("English")

elif page == "Heat-Seeking":
    from pages.heat_seeking import show
    show("English")

elif page == "Rain Predict":
    from pages.rain_prediction import show
    show("English")

elif page == "Forest":
    from pages.forest_layer import show
    show("English")

elif page == "Underground":
    from pages.underground import show
    show("English")

elif page == "AI Assistant":
    from pages.chatbot import show
    show("English")

elif page == "Validation":
    from pages.validation import show
    show("English")