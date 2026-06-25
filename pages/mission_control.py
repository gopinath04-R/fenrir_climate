import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from datetime import datetime

# ── Real Weather API (OpenMeteo — Free, No Key) ──────────
@st.cache_data(ttl=1800)  # Cache 30 mins
def get_weather(lat, lon):
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "daily": ["precipitation_probability_max",
                          "temperature_2m_max",
                          "temperature_2m_min",
                          "weathercode"],
                "timezone": "Asia/Kolkata",
                "forecast_days": 1
            }, timeout=5
        )
        d = r.json()["daily"]
        return {
            "rain_prob": d["precipitation_probability_max"][0],
            "tmax":      d["temperature_2m_max"][0],
            "tmin":      d["temperature_2m_min"][0],
            "code":      d["weathercode"][0]
        }
    except:
        return None

def weather_icon(code):
    if code is None: return "🌡️"
    if code == 0: return "☀️"
    if code <= 3: return "⛅"
    if code <= 67: return "🌧️"
    if code <= 77: return "❄️"
    if code <= 82: return "🌦️"
    return "⛈️"

def show(lang):

    # ── TOP NAVBAR ─────────────────────────────────────────
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    .top-nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 999;
      background: linear-gradient(90deg, #061020 0%, #0a1a30 50%, #061020 100%);
      border-bottom: 1px solid rgba(72,202,228,0.15);
      padding: 8px 32px;
      display: flex; align-items: center; gap: 0;
    }
    .nav-brand {
      font-family: 'Syne', sans-serif; font-size: 1.1em;
      font-weight: 800; letter-spacing: 4px; color: #48cae4;
      margin-right: 40px; white-space: nowrap;
    }
    .nav-links { display: flex; gap: 4px; flex: 1; }
    .nav-link {
      font-family: 'Space Grotesk', sans-serif; font-size: 0.72em;
      font-weight: 500; letter-spacing: 1px; color: #9ec4d4;
      padding: 6px 14px; border-radius: 6px; cursor: pointer;
      border: 1px solid transparent; transition: all 0.2s;
      text-decoration: none; white-space: nowrap;
    }
    .nav-link:hover, .nav-link.active {
      color: #48cae4; border-color: rgba(72,202,228,0.2);
      background: rgba(72,202,228,0.08);
    }
    .nav-time {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72em; color: #5a8a9f; margin-left: auto;
      white-space: nowrap;
    }
    .main-content { margin-top: 56px; }
    </style>
    """, unsafe_allow_html=True)

    now = datetime.now()
    st.markdown(f"""
    <div class="top-nav">
      <div class="nav-brand">🌧️ FENRIR</div>
      <div class="nav-links">
        <span class="nav-link active">🌐 Mission Control</span>
        <span class="nav-link">🔥 Heat-Seeking</span>
        <span class="nav-link">🌧️ Rain Predict</span>
        <span class="nav-link">🌿 Forest</span>
        <span class="nav-link">💧 Underground</span>
        <span class="nav-link">🤖 AI Assistant</span>
        <span class="nav-link">✅ Validation</span>
      </div>
      <div class="nav-time">
        📅 {now.strftime('%d %b %Y')} &nbsp;|&nbsp; 🕐 {now.strftime('%H:%M')} IST
      </div>
    </div>
    <div class="main-content"></div>
    """, unsafe_allow_html=True)

    # ── HEADER ─────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#061828,#0a2240,#061828);
                border:1px solid rgba(72,202,228,0.12);border-radius:16px;
                padding:20px 32px;margin-bottom:20px;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;
                  background:linear-gradient(90deg,transparent,#52b788,#48cae4,#52b788,transparent);"></div>
      <div style="font-family:'Syne',sans-serif;font-size:1.6em;font-weight:800;
                  color:#48cae4;text-align:center;letter-spacing:5px;
                  text-shadow:0 0 30px rgba(72,202,228,0.3);">🌧️ BHARATH CLIMATE TWIN</div>
      <div style="font-family:'Space Grotesk',sans-serif;font-size:0.78em;
                  color:#9ec4d4;text-align:center;margin-top:5px;letter-spacing:2px;">
        AI-Powered 5-Layer Climate Intelligence · Real-Time India Data
      </div>
      <div style="text-align:center;margin-top:8px;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.65em;
                     background:rgba(82,183,136,0.15);border:1px solid rgba(82,183,136,0.3);
                     color:#52b788;padding:3px 12px;border-radius:20px;">
          🏆 Team Fenrir · Bharatiya Antariksh Hackathon 2026 · Challenge 05
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── METRICS ────────────────────────────────────────────
    c1,c2,c3,c4 = st.columns(4)
    for col,(val,label,sub,color) in zip([c1,c2,c3,c4],[
        ("85.6%","ML Accuracy","✓ Validated 2025","#48cae4"),
        ("83.3%","Heat-Seeking GPS","✓ +58.3% vs Random","#52b788"),
        ("89.6L","Training Rows","✓ 5 Years · Full India","#f4a261"),
        ("5","Data Layers","✓ Sky to Underground","#2ec4b6"),
    ]):
        col.markdown(f"""
        <div style="background:#0f1f35;border:1px solid rgba(72,202,228,0.1);
                    border-top:3px solid {color};border-radius:12px;
                    padding:18px;text-align:center;margin-bottom:16px;">
          <div style="font-family:'Syne',sans-serif;font-size:1.8em;
                      font-weight:700;color:{color};">{val}</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:0.72em;
                      color:#9ec4d4;margin-top:4px;">{label}</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.62em;
                      color:#52b788;margin-top:3px;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    col_map, col_right = st.columns([3,2])

    # ── CITY DATA WITH CORRECT CLIMATE ZONES ──────────────
    cities = [
        # lat, lon, city, state, zone_type, correct_desc
        (13.08,80.27,"Chennai","TN","coastal"),
        (19.07,72.87,"Mumbai","MH","coastal"),
        (12.97,77.59,"Bengaluru","KA","plateau"),
        (17.38,78.48,"Hyderabad","TS","plateau"),
        (28.61,77.20,"Delhi","DL","north_plains"),
        (22.57,88.36,"Kolkata","WB","east"),
        (26.91,75.78,"Jaipur","RJ","desert"),
        (23.25,77.41,"Bhopal","MP","central"),
        (21.16,79.09,"Nagpur","MH","central"),
        (26.84,80.94,"Lucknow","UP","north_plains"),
        (9.93, 76.26,"Kochi","KL","coastal"),
        (26.14,91.73,"Guwahati","AS","northeast"),
        (25.59,85.13,"Patna","BR","east"),
        (11.00,77.00,"Coimbatore","TN","western_ghats"),
        (20.27,85.83,"Bhubaneswar","OD","east"),
        (23.02,72.57,"Ahmedabad","GJ","arid"),
        # CORRECT — Snow/Cold zones
        (34.08,74.80,"Srinagar","JK","alpine_snow"),
        (32.71,74.86,"Jammu","JK","sub_himalayan"),
        (31.10,77.17,"Shimla","HP","alpine_snow"),
        (30.73,76.77,"Chandigarh","PB","north_plains"),
        (27.09,88.26,"Gangtok","SK","alpine_snow"),
        (27.46,94.91,"Dibrugarh","AS","northeast"),
        (8.50, 76.97,"Thiruvananthapuram","KL","coastal"),
    ]

    with col_map:
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                    letter-spacing:2px;color:#e8f4f8;padding-bottom:10px;
                    border-bottom:1px solid rgba(72,202,228,0.1);margin-bottom:14px;">
          🗺️ India Climate Map — Live Rain Probability Today
        </div>
        """, unsafe_allow_html=True)

        m = folium.Map(location=[22.0,80.0], zoom_start=5,
                       tiles="CartoDB dark_matter")

        live_alerts = []

        for lat,lon,city,state,zone in cities:
            w = get_weather(lat, lon)

            if w:
                prob = w["rain_prob"]
                tmax = w["tmax"]
                tmin = w["tmin"]
                code = w["code"]
                icon = weather_icon(code)
                data_tag = "🛰️ Live"
            else:
                # Fallback climate zone estimates
                zone_prob = {
                    "coastal":55,"east":60,"northeast":70,
                    "plateau":35,"north_plains":30,"central":40,
                    "desert":8,"arid":12,"western_ghats":65,
                    "alpine_snow":20,"sub_himalayan":25
                }
                prob = zone_prob.get(zone, 40)
                tmax = {"alpine_snow":12,"sub_himalayan":22,
                        "desert":44,"coastal":35}.get(zone, 32)
                tmin = tmax - 10
                icon = "⛅"
                data_tag = "📊 Est."

            # Color based on rain probability
            if prob >= 65:
                color="#48cae4"; risk="HIGH RAIN"
            elif prob >= 35:
                color="#f4a261"; risk="MODERATE"
            else:
                # Special for snow zones
                if zone == "alpine_snow":
                    color="#caf0f8"; risk="SNOW/COLD"
                elif zone == "sub_himalayan":
                    color="#90e0ef"; risk="COOL/CLOUDY"
                else:
                    color="#e76f51"; risk="DRY/LOW"

            # Build live alerts
            if prob >= 70:
                live_alerts.append((city,state,prob,tmax,"FLOOD WATCH","#48cae4","rgba(30,96,145,0.2)"))
            elif zone in ["alpine_snow"] and tmax < 15:
                live_alerts.append((city,state,prob,tmax,"SNOW/COLD","#caf0f8","rgba(202,240,248,0.1)"))

            folium.CircleMarker(
                location=[lat,lon],
                radius=11 if prob>=65 else 8,
                color=color, fill=True, fill_color=color,
                fill_opacity=0.8, weight=2,
                tooltip=f"{icon} {city} — {prob}% rain",
                popup=folium.Popup(f"""
                <div style="background:#0f1f35;color:#e8f4f8;padding:10px;
                            border-radius:8px;font-family:Arial;min-width:170px;
                            border:1px solid {color};">
                  <b style="color:{color};">{icon} {city}, {state}</b><br>
                  <hr style="border-color:rgba(255,255,255,0.1);margin:4px 0;">
                  🌧️ Rain Today: <b style="color:{color};">{prob}%</b><br>
                  🌡️ Max: <b>{tmax}°C</b> · Min: <b>{tmin}°C</b><br>
                  ⚡ Status: <b style="color:{color};">{risk}</b><br>
                  <span style="font-size:10px;color:#5a8a9f;">{data_tag} · OpenMeteo</span>
                </div>
                """, max_width=200)
            ).add_to(m)

        st_folium(m, width=700, height=460, returned_objects=[])
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65em;color:#5a8a9f;
                    margin-top:6px;padding:5px 10px;background:rgba(72,202,228,0.04);
                    border-radius:6px;border:1px solid rgba(72,202,228,0.08);">
          🛰️ Live data: OpenMeteo API · Updated every 30min · Click markers for details
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        # ── LIVE RAIN ALERTS — REAL DATA ──────────────────
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                    letter-spacing:2px;color:#e8f4f8;padding-bottom:10px;
                    border-bottom:1px solid rgba(72,202,228,0.1);margin-bottom:14px;">
          ⚡ Today's Rain Chance — Live
        </div>
        """, unsafe_allow_html=True)

        # Show real weather for key cities
        key_cities = [
            (13.08,80.27,"Chennai","TN","coastal"),
            (9.93,76.26,"Kochi","KL","coastal"),
            (26.14,91.73,"Guwahati","AS","northeast"),
            (22.57,88.36,"Kolkata","WB","east"),
            (28.61,77.20,"Delhi","DL","north_plains"),
            (26.91,75.78,"Jaipur","RJ","desert"),
            (34.08,74.80,"Srinagar","JK","alpine_snow"),
            (19.07,72.87,"Mumbai","MH","coastal"),
        ]

        for lat,lon,city,state,zone in key_cities:
            w = get_weather(lat,lon)
            if w:
                prob = w["rain_prob"]
                tmax = w["tmax"]
                icon = weather_icon(w["code"])
                tag = "🛰️ Live"
            else:
                zp={"coastal":55,"northeast":70,"east":60,
                    "north_plains":30,"desert":8,"alpine_snow":20}
                prob=zp.get(zone,40)
                tmax=32; icon="⛅"; tag="📊 Est."

            if prob>=65: color="#48cae4"; bar_w=prob
            elif prob>=35: color="#f4a261"; bar_w=prob
            else:
                color="#90e0ef" if zone=="alpine_snow" else "#e76f51"
                bar_w=max(prob,5)

            st.markdown(f"""
            <div style="background:#0f1f35;border:1px solid rgba(72,202,228,0.08);
                        border-radius:8px;padding:9px 13px;margin-bottom:6px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:0.8em;
                               font-weight:600;color:#e8f4f8;">{icon} {city}, {state}</span>
                  <span style="font-family:'JetBrains Mono',monospace;font-size:0.6em;
                               color:#5a8a9f;margin-left:6px;">{tag}</span>
                </div>
                <div style="font-family:'Syne',sans-serif;font-size:0.9em;
                            font-weight:700;color:{color};">{prob}%</div>
              </div>
              <div style="background:rgba(72,202,228,0.08);border-radius:4px;
                          height:4px;margin-top:6px;overflow:hidden;">
                <div style="background:{color};width:{bar_w}%;height:100%;
                            border-radius:4px;transition:width 0.5s;"></div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:0.6em;
                          color:#5a8a9f;margin-top:3px;">🌡️ {tmax}°C today</div>
            </div>
            """, unsafe_allow_html=True)

        # Layer Status
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                    letter-spacing:2px;color:#e8f4f8;padding-bottom:10px;margin-top:16px;
                    border-bottom:1px solid rgba(72,202,228,0.1);margin-bottom:14px;">
          🔋 Layer Status
        </div>
        """, unsafe_allow_html=True)

        layers=[
            ("☀️","Solar","ERA5+MOSDAC","#f4a261","green"),
            ("🌬️","Atmosphere","ERA5 Wind","#48cae4","green"),
            ("🌿","Surface NDVI","Bhuvan LULC","#52b788","yellow"),
            ("🔥","Hardpan","ISRO Thermal","#e76f51","green"),
            ("💧","Underground","CGWB 32 States","#2ec4b6","green"),
        ]
        for icon,name,src,color,dot in layers:
            dc="#52b788" if dot=="green" else "#ffd166"
            st.markdown(f"""
            <div style="background:#0f1f35;border:1px solid rgba(72,202,228,0.08);
                        border-radius:7px;padding:8px 12px;margin-bottom:5px;
                        display:flex;align-items:center;gap:8px;">
              <span>{icon}</span>
              <div style="flex:1;">
                <div style="font-family:'Space Grotesk',sans-serif;font-size:0.78em;
                            font-weight:600;color:#e8f4f8;">{name}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.62em;
                            color:#5a8a9f;">{src}</div>
              </div>
              <span style="width:7px;height:7px;background:{dc};border-radius:50%;
                           box-shadow:0 0 5px {dc};display:inline-block;"></span>
            </div>
            """, unsafe_allow_html=True)