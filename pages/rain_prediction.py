import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pickle

# ── REAL LIVE WEATHER — OpenMeteo (Free, No Key) ─────────
@st.cache_data(ttl=1800)
def get_live_forecast(lat, lon):
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": [
                    "precipitation_probability_max",
                    "precipitation_sum",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "weathercode",
                    "windspeed_10m_max",
                    "et0_fao_evapotranspiration"
                ],
                "hourly": ["temperature_2m","precipitation_probability"],
                "timezone": "Asia/Kolkata",
                "forecast_days": 7
            },
            timeout=8
        )
        data = r.json()
        daily = data["daily"]
        return {
            "dates":     daily["time"],
            "rain_prob": daily["precipitation_probability_max"],
            "rain_mm":   daily["precipitation_sum"],
            "tmax":      daily["temperature_2m_max"],
            "tmin":      daily["temperature_2m_min"],
            "wcode":     daily["weathercode"],
            "wind":      daily["windspeed_10m_max"],
            "evap":      daily["et0_fao_evapotranspiration"],
            "success":   True
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@st.cache_data(ttl=3600)
def get_historical_temp(lat, lon):
    """Get real historical temperature from ERA5 via OpenMeteo"""
    try:
        end = datetime.now()
        start = end - timedelta(days=365)
        r = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={
                "latitude": lat, "longitude": lon,
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date":   end.strftime("%Y-%m-%d"),
                "daily": ["temperature_2m_max","temperature_2m_min",
                          "precipitation_sum"],
                "timezone": "Asia/Kolkata"
            },
            timeout=10
        )
        d = r.json()["daily"]
        df = pd.DataFrame({
            "date":  pd.to_datetime(d["time"]),
            "tmax":  d["temperature_2m_max"],
            "tmin":  d["temperature_2m_min"],
            "rain":  d["precipitation_sum"]
        })
        df["month"] = df["date"].dt.month
        return df
    except:
        return None

def weather_icon(code):
    if code == 0:  return "☀️"
    if code <= 3:  return "⛅"
    if code <= 45: return "🌫️"
    if code <= 67: return "🌧️"
    if code <= 77: return "❄️"
    if code <= 82: return "🌦️"
    return "⛈️"

def weather_label(code):
    if code == 0:  return "Clear Sky"
    if code <= 3:  return "Partly Cloudy"
    if code <= 45: return "Foggy"
    if code <= 67: return "Rainy"
    if code <= 77: return "Snow"
    if code <= 82: return "Rain Showers"
    return "Thunderstorm"

DISTRICTS = {
    "Chennai (TN - Coastal)":         {"lat":13.08,"lon":80.27,"zone":"Coastal"},
    "Mumbai (MH - Coastal)":          {"lat":19.07,"lon":72.87,"zone":"Coastal"},
    "Delhi (DL - North Plains)":      {"lat":28.61,"lon":77.20,"zone":"North Plains"},
    "Kolkata (WB - East)":            {"lat":22.57,"lon":88.36,"zone":"East"},
    "Bengaluru (KA - Plateau)":       {"lat":12.97,"lon":77.59,"zone":"Plateau"},
    "Hyderabad (TS - Plateau)":       {"lat":17.38,"lon":78.48,"zone":"Plateau"},
    "Jaipur (RJ - Desert)":           {"lat":26.91,"lon":75.78,"zone":"Desert"},
    "Kochi (KL - Coastal)":           {"lat":9.93, "lon":76.26,"zone":"Coastal"},
    "Guwahati (AS - Northeast)":      {"lat":26.14,"lon":91.73,"zone":"Northeast"},
    "Nagpur (MH - Central)":          {"lat":21.16,"lon":79.09,"zone":"Central"},
    "Patna (BR - East)":              {"lat":25.59,"lon":85.13,"zone":"East"},
    "Bhopal (MP - Central)":          {"lat":23.25,"lon":77.41,"zone":"Central"},
    "Srinagar (JK - Alpine)":         {"lat":34.08,"lon":74.80,"zone":"Alpine"},
    "Shimla (HP - Alpine)":           {"lat":31.10,"lon":77.17,"zone":"Alpine"},
    "Coimbatore (TN - W.Ghats)":      {"lat":11.00,"lon":77.00,"zone":"Western Ghats"},
    "Pune (MH - W.Ghats)":            {"lat":18.52,"lon":73.86,"zone":"Western Ghats"},
    "Ahmedabad (GJ - Arid)":          {"lat":23.02,"lon":72.57,"zone":"Arid"},
    "Jaisalmer (RJ - Desert)":        {"lat":26.91,"lon":70.90,"zone":"Desert"},
    "Bhubaneswar (OD - East)":        {"lat":20.27,"lon":85.83,"zone":"East"},
    "Thiruvananthapuram (KL)":        {"lat":8.50, "lon":76.97,"zone":"Coastal"},
    "Visakhapatnam (AP - Coastal)":   {"lat":17.68,"lon":83.21,"zone":"Coastal"},
    "Lucknow (UP - North)":           {"lat":26.84,"lon":80.94,"zone":"North Plains"},
    "Dibrugarh (AS - Northeast)":     {"lat":27.46,"lon":94.91,"zone":"Northeast"},
    "Gangtok (SK - Alpine)":          {"lat":27.33,"lon":88.61,"zone":"Alpine"},
}

def show(lang):
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#061828,#0a2240,#061828);
                border:1px solid rgba(72,202,228,0.15);border-radius:16px;
                padding:22px 30px;margin-bottom:20px;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;
                  background:linear-gradient(90deg,transparent,#48cae4,#90e0ef,#48cae4,transparent);"></div>
      <div style="font-family:'Syne',sans-serif;font-size:1.4em;font-weight:800;
                  color:#48cae4;letter-spacing:3px;">🌧️ Rain Prediction Engine</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.7em;
                  color:#9ec4d4;margin-top:5px;">
        🛰️ Live OpenMeteo API · ERA5 Reanalysis · Real 7-Day Forecast · No fake data!
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1,1])

    with col_left:
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                    letter-spacing:2px;color:#e8f4f8;padding-bottom:10px;
                    border-bottom:1px solid rgba(72,202,228,0.1);margin-bottom:14px;">
          📍 Select Location
        </div>
        """, unsafe_allow_html=True)

        sel = st.selectbox("📍 District", list(DISTRICTS.keys()),
                           label_visibility="collapsed")
        info = DISTRICTS[sel]
        lat, lon, zone = info["lat"], info["lon"], info["zone"]

        st.markdown(f"""
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.7em;color:#48cae4;
                    padding:6px 12px;background:rgba(72,202,228,0.06);border-radius:6px;
                    border:1px solid rgba(72,202,228,0.12);margin-bottom:14px;">
          📍 {lat}°N, {lon}°E · Zone: {zone}
        </div>
        """, unsafe_allow_html=True)

        # Fetch live data
        with st.spinner("🛰️ Fetching live data from OpenMeteo..."):
            forecast = get_live_forecast(lat, lon)

        if forecast["success"]:
            today = forecast
            prob0  = today["rain_prob"][0]
            tmax0  = today["tmax"][0]
            tmin0  = today["tmin"][0]
            rain0  = today["rain_mm"][0]
            code0  = today["wcode"][0]
            wind0  = today["wind"][0]

            # Today's card
            if prob0 >= 65:
                bg="rgba(30,96,145,0.25)"; border="#48cae4"; emoji="🌧️"; status="RAIN EXPECTED"
            elif prob0 >= 35:
                bg="rgba(244,162,97,0.15)"; border="#f4a261"; emoji="🌦️"; status="POSSIBLE RAIN"
            elif zone == "Alpine":
                bg="rgba(202,240,248,0.1)"; border="#caf0f8"; emoji="❄️"; status="SNOW/COLD"
            else:
                bg="rgba(231,111,81,0.12)"; border="#e76f51"; emoji="☀️"; status="DRY / LOW"

            now = datetime.now()
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border};
                        border-radius:14px;padding:18px;text-align:center;margin-bottom:14px;">
              <div style="font-family:'JetBrains Mono',monospace;font-size:0.62em;
                          color:#5a8a9f;margin-bottom:6px;">
                🛰️ LIVE · {now.strftime('%d %b %Y %H:%M')} IST
              </div>
              <div style="font-size:2.2em;">{weather_icon(code0)}</div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:0.72em;
                          color:#9ec4d4;margin-top:2px;">{weather_label(code0)}</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.3em;font-weight:800;
                          color:{border};letter-spacing:2px;margin-top:8px;">{status}</div>
              <div style="font-family:'Syne',sans-serif;font-size:2em;font-weight:700;
                          color:{border};margin-top:4px;">{prob0}%</div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:0.72em;
                          color:#9ec4d4;margin-top:4px;">Rain Probability Today</div>
            </div>
            """, unsafe_allow_html=True)

            # Live stats grid
            stats = [
                ("🌡️ Max Temp", f"{tmax0}°C", "#f4a261"),
                ("🌡️ Min Temp", f"{tmin0}°C", "#48cae4"),
                ("💧 Rain (mm)", f"{rain0}mm",  "#2ec4b6"),
                ("💨 Wind",     f"{wind0}km/h","#9ec4d4"),
            ]
            sc1,sc2,sc3,sc4 = st.columns(4)
            for col,(label,val,color) in zip([sc1,sc2,sc3,sc4],stats):
                col.markdown(f"""
                <div style="background:#0f1f35;border:1px solid rgba(72,202,228,0.1);
                            border-radius:8px;padding:10px;text-align:center;">
                  <div style="font-family:'Syne',sans-serif;font-size:1.1em;
                              font-weight:700;color:{color};">{val}</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:0.6em;
                              color:#5a8a9f;margin-top:2px;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Rain gauge
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob0,
                title={"text":"Rain Probability %",
                       "font":{"color":"white","size":12}},
                gauge={
                    "axis":{"range":[0,100],"tickcolor":"white"},
                    "bar":{"color":border,"thickness":0.28},
                    "bgcolor":"#0f1f35",
                    "steps":[
                        {"range":[0,30],"color":"rgba(231,111,81,0.25)"},
                        {"range":[30,60],"color":"rgba(244,162,97,0.2)"},
                        {"range":[60,100],"color":"rgba(72,202,228,0.25)"},
                    ],
                    "threshold":{"line":{"color":"white","width":2},"value":50}
                },
                number={"suffix":"%","font":{"color":border,"size":26}}
            ))
            fig_g.update_layout(
                plot_bgcolor="#0f1f35",paper_bgcolor="#0f1f35",
                height=200,margin=dict(t=40,b=5,l=20,r=20),
                font_color="white"
            )
            st.plotly_chart(fig_g, use_container_width=True)

        else:
            st.error(f"⚠️ API Error: {forecast.get('error','Unknown')}. Check internet connection.")

    with col_right:
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                    letter-spacing:2px;color:#e8f4f8;padding-bottom:10px;
                    border-bottom:1px solid rgba(72,202,228,0.1);margin-bottom:14px;">
          📅 7-Day Live Forecast
        </div>
        """, unsafe_allow_html=True)

        if forecast["success"]:
            # 7-day forecast cards
            for i in range(7):
                date_str = forecast["dates"][i]
                date_obj = datetime.strptime(date_str,"%Y-%m-%d")
                day_name = "Today" if i==0 else "Tomorrow" if i==1 \
                           else date_obj.strftime("%a %d %b")
                prob  = forecast["rain_prob"][i]
                tmax  = forecast["tmax"][i]
                tmin  = forecast["tmin"][i]
                rain  = forecast["rain_mm"][i]
                code  = forecast["wcode"][i]
                icon  = weather_icon(code)

                if prob>=65: bar_c="#48cae4"
                elif prob>=35: bar_c="#f4a261"
                else: bar_c="#e76f51" if zone!="Alpine" else "#caf0f8"

                st.markdown(f"""
                <div style="background:#0f1f35;border:1px solid rgba(72,202,228,0.08);
                            border-radius:8px;padding:9px 13px;margin-bottom:5px;
                            display:flex;align-items:center;gap:10px;">
                  <div style="font-size:1.3em;width:28px;text-align:center;">{icon}</div>
                  <div style="flex:1;">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:0.78em;
                                font-weight:600;color:#e8f4f8;">{day_name}</div>
                    <div style="background:rgba(72,202,228,0.08);border-radius:3px;
                                height:4px;margin-top:4px;overflow:hidden;">
                      <div style="background:{bar_c};width:{prob}%;height:100%;
                                  border-radius:3px;"></div>
                    </div>
                  </div>
                  <div style="text-align:right;min-width:80px;">
                    <div style="font-family:'Syne',sans-serif;font-size:0.9em;
                                font-weight:700;color:{bar_c};">{prob}%</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.62em;
                                color:#5a8a9f;">{tmax}°/{tmin}° · {rain}mm</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # Historical chart — REAL ERA5 data
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                letter-spacing:2px;color:#e8f4f8;padding-bottom:10px;
                border-bottom:1px solid rgba(72,202,228,0.1);margin-bottom:14px;">
      📈 Real Historical Temperature — Past 12 Months (ERA5)
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("📡 Loading ERA5 historical data..."):
        hist_df = get_historical_temp(lat, lon)

    if hist_df is not None:
        monthly = hist_df.groupby("month").agg(
            tmax=("tmax","mean"), tmin=("tmin","mean"),
            rain=("rain","sum")
        ).reset_index()
        months_label=["Jan","Feb","Mar","Apr","May","Jun",
                      "Jul","Aug","Sep","Oct","Nov","Dec"]
        monthly["month_name"]=[months_label[m-1] for m in monthly["month"]]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=monthly["month_name"], y=monthly["tmax"],
            name="Max Temp (°C)", mode="lines+markers",
            line=dict(color="#f4a261",width=2),
            marker=dict(size=6)
        ))
        fig2.add_trace(go.Scatter(
            x=monthly["month_name"], y=monthly["tmin"],
            name="Min Temp (°C)", mode="lines+markers",
            line=dict(color="#48cae4",width=2),
            marker=dict(size=6),
            fill="tonexty",
            fillcolor="rgba(72,202,228,0.05)"
        ))
        fig2.update_layout(
            plot_bgcolor="#0f1f35",paper_bgcolor="#0f1f35",
            font_color="white",height=240,
            margin=dict(t=10,b=10,l=40,r=10),
            legend=dict(font=dict(size=10,color="white")),
            yaxis=dict(title="Temp °C",
                      gridcolor="rgba(72,202,228,0.1)"),
            xaxis=dict(gridcolor="rgba(72,202,228,0.06)")
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Monthly rainfall bar
        fig3 = go.Figure(go.Bar(
            x=monthly["month_name"],
            y=monthly["rain"],
            marker_color=[
                "#48cae4" if r>100 else "#f4a261" if r>30 else "#e76f51"
                for r in monthly["rain"]
            ],
            text=[f"{r:.0f}mm" for r in monthly["rain"]],
            textposition="outside",
            textfont=dict(size=9,color="white")
        ))
        fig3.update_layout(
            plot_bgcolor="#0f1f35",paper_bgcolor="#0f1f35",
            font_color="white",height=220,
            margin=dict(t=20,b=10,l=40,r=10),
            yaxis=dict(title="Monthly Rainfall (mm)",
                      gridcolor="rgba(72,202,228,0.1)"),
            title=dict(text="Monthly Rainfall Distribution (ERA5 · Past 12 months)",
                      font=dict(size=11,color="#9ec4d4"))
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65em;color:#5a8a9f;
                    padding:6px 10px;background:rgba(72,202,228,0.04);
                    border-radius:6px;border:1px solid rgba(72,202,228,0.08);">
          📡 Real ERA5 reanalysis data · OpenMeteo Archive API ·
          Not fake/static — actual measured historical records!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Historical data temporarily unavailable. Live forecast above is still real!")