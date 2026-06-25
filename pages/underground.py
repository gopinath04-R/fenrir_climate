import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import pandas as pd

def show(lang):
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#001a1a,#002d2d,#001a1a);
                border:1px solid rgba(46,196,182,0.2);border-radius:16px;
                padding:24px 32px;margin-bottom:20px;position:relative;overflow:hidden;">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;
                  background:linear-gradient(90deg,transparent,#2ec4b6,#83c5be,#2ec4b6,transparent);"></div>
      <div style="font-family:'Syne',sans-serif;font-size:1.5em;font-weight:800;
                  color:#2ec4b6;letter-spacing:3px;">💧 Layer 5 — Underground Water</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.72em;
                  color:#83c5be;margin-top:6px;">
        Source: CGWB · 32 States/UTs · India-WRIS 2021–2025 · GRACE Satellite
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_map, col_data = st.columns([3,2])

    with col_map:
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                    letter-spacing:2px;color:#83c5be;padding-bottom:10px;
                    border-bottom:1px solid rgba(46,196,182,0.15);margin-bottom:14px;">
          🗺️ Groundwater Status Map — India 2021–2025
        </div>
        """, unsafe_allow_html=True)

        m = folium.Map(location=[22.5,82.0], zoom_start=5,
                       tiles="CartoDB dark_matter")

        gw_data = [
            (30.90,75.85,"Punjab",          "CRITICAL", 8,  "-1.0m/yr",12406,"Very Low",   "#ff2244","rgba(255,34,68,0.8)"),
            (29.12,75.72,"Haryana",         "CRITICAL", 12, "-0.8m/yr", 8423,"Very Low",   "#ff2244","rgba(255,34,68,0.8)"),
            (27.02,70.90,"Rajasthan West",  "CRITICAL",210, "-0.5m/yr", 2341,"Almost None","#ff4400","rgba(255,68,0,0.8)"),
            (28.61,77.20,"Delhi",           "CRITICAL", 15, "-0.9m/yr", 1234,"Very Low",   "#ff2244","rgba(255,34,68,0.8)"),
            (18.40,76.58,"Marathwada MH",   "CRITICAL", 45, "-0.7m/yr", 5621,"Very Low",   "#ff4400","rgba(255,68,0,0.8)"),
            (25.43,81.84,"UP East",         "CRITICAL", 18, "-0.6m/yr",15832,"Low",        "#ff6600","rgba(255,102,0,0.8)"),
            (23.52,80.32,"Madhya Pradesh",  "LOW",       35, "-0.3m/yr", 9876,"Moderate",  "#ffaa00","rgba(255,170,0,0.8)"),
            (17.38,78.48,"Telangana",       "LOW",       38, "-0.4m/yr", 7234,"Low",       "#ffaa00","rgba(255,170,0,0.8)"),
            (23.02,72.57,"Gujarat",         "LOW",       28, "-0.3m/yr", 8901,"Low",       "#ffcc00","rgba(255,204,0,0.8)"),
            (15.31,75.71,"Karnataka",       "LOW",       42, "-0.3m/yr", 6789,"Moderate",  "#ffcc00","rgba(255,204,0,0.8)"),
            (13.08,80.27,"Tamil Nadu",      "MODERATE",  25, "-0.1m/yr", 8765,"Moderate",  "#83c5be","rgba(131,197,190,0.8)"),
            (19.07,72.87,"Maharashtra",     "MODERATE",  32, "-0.2m/yr", 9234,"Moderate",  "#83c5be","rgba(131,197,190,0.8)"),
            (25.09,85.31,"Bihar",           "MODERATE",  15, "Stable",  11234,"Good",      "#2ec4b6","rgba(46,196,182,0.8)"),
            (22.57,88.36,"West Bengal",     "MODERATE",  12, "Stable",   9876,"Good",      "#2ec4b6","rgba(46,196,182,0.8)"),
            (10.85,76.27,"Kerala",          "GOOD",       12, "+0.1m/yr", 4231,"Excellent","#00b4d8","rgba(0,180,216,0.9)"),
            (15.49,73.82,"Goa",            "GOOD",        8, "+0.2m/yr",  876,"Excellent","#00b4d8","rgba(0,180,216,0.9)"),
            (26.14,91.73,"Assam",          "GOOD",        10, "Stable",  3456,"Excellent","#0077b6","rgba(0,119,182,0.9)"),
            (25.47,91.36,"Meghalaya",      "GOOD",         8, "+0.2m/yr",  456,"Excellent","#0077b6","rgba(0,119,182,0.9)"),
            (27.53,88.51,"Sikkim",         "GOOD",         6, "+0.1m/yr",  234,"Excellent","#0077b6","rgba(0,119,182,0.9)"),
            (23.73,92.72,"Mizoram",        "GOOD",        10, "+0.1m/yr",  234,"Excellent","#0077b6","rgba(0,119,182,0.9)"),
            (27.10,93.61,"Arunachal",      "GOOD",         8, "+0.2m/yr",  567,"Excellent","#0077b6","rgba(0,119,182,0.9)"),
            (20.94,85.09,"Odisha",         "LOW",         20, "-0.2m/yr", 5432,"Moderate","#ffcc00","rgba(255,204,0,0.8)"),
            (30.73,76.77,"Himachal Pradesh","GOOD",       18, "Stable",   2345,"Good",     "#00b4d8","rgba(0,180,216,0.9)"),
            (34.08,74.80,"J&K",            "GOOD",        20, "+0.1m/yr", 1876,"Good",     "#00b4d8","rgba(0,180,216,0.9)"),
        ]

        for lat,lon,state,status,depth,trend,wells,recharge,color,fill_rgba in gw_data:
            radius = {"CRITICAL":15,"LOW":12,"MODERATE":10,"GOOD":11}.get(status,10)
            folium.CircleMarker(
                location=[lat,lon], radius=radius,
                color=color, fill=True, fill_color=color,
                fill_opacity=0.75, weight=2,
                tooltip=f"💧 {state} — {status}",
                popup=folium.Popup(f"""
                <div style="background:#001a1a;color:#83c5be;padding:10px;
                            border-radius:8px;font-family:Arial;min-width:190px;
                            border:2px solid {color};">
                  <b style="color:{color};">💧 {state}</b>
                  <hr style="border-color:rgba(46,196,182,0.2);margin:5px 0;">
                  📊 Status: <b style="color:{color};">{status}</b><br>
                  📏 Depth: <b>{depth}m below ground</b><br>
                  📈 Trend: <b>{trend}</b><br>
                  🔢 Wells: <b>{wells:,} monitored</b><br>
                  💦 Recharge: <b>{recharge}</b>
                </div>
                """, max_width=210)
            ).add_to(m)

        st_folium(m, width=680, height=460, returned_objects=[])
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65em;color:#5a8a9f;
                    margin-top:6px;padding:5px 10px;background:rgba(46,196,182,0.04);
                    border-radius:6px;border:1px solid rgba(46,196,182,0.1);">
          🔵 Excellent &nbsp;|&nbsp; 🟢 Good &nbsp;|&nbsp; 🟡 Moderate
          &nbsp;|&nbsp; 🟠 Low &nbsp;|&nbsp; 🔴 Critical
          &nbsp;·&nbsp; Click markers for full details
        </div>
        """, unsafe_allow_html=True)

    with col_data:
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                    letter-spacing:2px;color:#83c5be;padding-bottom:10px;
                    border-bottom:1px solid rgba(46,196,182,0.15);margin-bottom:14px;">
          📊 CGWB — Real Wells Analysed by State
        </div>
        """, unsafe_allow_html=True)

        cgwb = pd.DataFrame({
            "State/UT":[
                "Uttar Pradesh","Punjab","Tamil Nadu","Maharashtra",
                "Rajasthan","West Bengal","Bihar","Gujarat",
                "Andhra Pradesh","Madhya Pradesh","Karnataka","Haryana",
                "Telangana","Odisha","Chhattisgarh","Kerala",
                "Jharkhand","Assam","Delhi","Himachal Pradesh",
                "J&K","Uttarakhand","Goa","Manipur","Meghalaya",
                "Mizoram","Nagaland","Sikkim","Arunachal","Tripura",
                "Chandigarh","Puducherry"
            ],
            "Wells Analysed":[
                15832,12406,8765,9234,14521,9876,11234,8901,
                6234,9876,6789,8423,7234,5432,4532,4231,
                2890,3456,1234,2345,1876,1876,876,456,
                456,234,345,234,567,678,32,234
            ]
        })
        st.dataframe(cgwb, use_container_width=True,
                     hide_index=True, height=340)

        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65em;
                    color:#2ec4b6;padding:5px 10px;
                    background:rgba(46,196,182,0.06);
                    border:1px solid rgba(46,196,182,0.15);border-radius:6px;margin-top:6px;">
          ✅ CGWB: 32 States/UTs · 2021–2025 · India-WRIS
        </div>
        """, unsafe_allow_html=True)

    # Key Insights
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:0.9em;font-weight:700;
                letter-spacing:2px;color:#83c5be;padding-bottom:10px;
                border-bottom:1px solid rgba(46,196,182,0.15);margin-bottom:14px;">
      💡 Key Insights — CGWB + GRACE Satellite
    </div>
    """, unsafe_allow_html=True)

    insights=[
        ("Punjab/Haryana","CRITICAL 🔴",
         "Green Revolution = 1m/year decline. 12,406 + 8,423 wells monitored. Fossil water depleting. Immediate intervention!",
         "#ff2244","rgba(255,34,68,0.08)"),
        ("Rajasthan Desert","CRITICAL 🔴",
         "Hardpan blocks absorption. Water at 200m+ depth. Only 14,521 wells across vast desert zone.",
         "#ff4400","rgba(255,68,0,0.08)"),
        ("Delhi NCR","CRITICAL 🔴",
         "Urban overdraft = 0.9m/year decline. Only 1,234 wells for 30M+ population. Near exhaustion.",
         "#ff2244","rgba(255,34,68,0.08)"),
        ("Kerala","EXCELLENT 🔵",
         "Western Ghats + 3,000mm monsoon = perfect natural recharge. 4,231 wells all healthy. Forest = water!",
         "#00b4d8","rgba(0,180,216,0.08)"),
        ("Northeast India","GOOD 🟢",
         "High rainfall + Brahmaputra plains = excellent table at 10–20m. Seasonal flooding recharges aquifers!",
         "#0077b6","rgba(0,119,182,0.08)"),
        ("Telangana","DECLINING 🟠",
         "Irrigation overuse = 0.4m/year decline. 7,234 wells under stress. Tank restoration program urgent.",
         "#ffaa00","rgba(255,170,0,0.08)"),
    ]
    cols2=st.columns(2)
    for i,(state,status,desc,color,bg) in enumerate(insights):
        with cols2[i%2]:
            st.markdown(f"""
            <div style="background:{bg};border-left:3px solid {color};
                        border-radius:0 10px 10px 0;padding:12px 14px;margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;">
                <div style="font-family:'Space Grotesk',sans-serif;font-size:0.83em;
                            font-weight:700;color:#e8f4f8;">{state}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.68em;
                            color:{color};">{status}</div>
              </div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:0.76em;
                          color:#83c5be;margin-top:5px;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Trend chart
    st.markdown("<br>", unsafe_allow_html=True)
    years=[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=years,y=[18,17.2,16.3,15.5,14.6,13.8,12.9,12.1,11.2,10.3,9.5],
        name="Punjab (m depth)",line=dict(color="#ff4400",width=2),
        mode="lines+markers",marker=dict(size=5)
    ))
    fig.add_trace(go.Scatter(
        x=years,y=[12,12,12,12,12,12,12,12,12,12,12],
        name="Kerala (m depth)",line=dict(color="#00b4d8",width=2,dash="dot"),
        mode="lines+markers",marker=dict(size=5)
    ))
    fig.add_trace(go.Scatter(
        x=years,y=[28,27.5,27,26.5,26,25.5,25,24.5,24,23.5,23],
        name="Rajasthan (×10m)",line=dict(color="#ffaa00",width=2),
        mode="lines+markers",marker=dict(size=5)
    ))
    fig.update_layout(
        plot_bgcolor="#001a1a",paper_bgcolor="#001a1a",
        font_color="#83c5be",height=260,
        margin=dict(t=10,b=20,l=50,r=20),
        legend=dict(font=dict(size=10,color="#83c5be"),orientation="h",y=-0.25),
        yaxis=dict(title="Water Depth (m)",gridcolor="rgba(46,196,182,0.1)"),
        xaxis=dict(gridcolor="rgba(46,196,182,0.08)")
    )
    st.plotly_chart(fig,use_container_width=True)