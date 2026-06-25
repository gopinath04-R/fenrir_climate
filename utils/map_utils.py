import folium
from folium import plugins
import math

def create_india_map(zoom=5, tiles='CartoDB dark_matter'):
    m = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=zoom,
        tiles=tiles,
        prefer_canvas=True
    )
    # Add satellite layer option
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='ESRI Satellite',
        name='🛰️ Satellite View',
        overlay=False
    ).add_to(m)
    folium.LayerControl().add_to(m)
    return m

def add_rain_marker(m, lat, lon, city, prob, color):
    # Pulse effect for high rain
    if prob > 0.65:
        plugins.CirclePattern(m) if hasattr(plugins, 'CirclePattern') else None
    
    folium.CircleMarker(
        location=[lat, lon],
        radius=14,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.75,
        weight=2,
        popup=folium.Popup(
            f"""<div style='font-family:Arial;background:#1a1a2e;color:white;padding:10px;border-radius:8px;min-width:150px'>
            <b style='color:#4fc3f7;font-size:14px'>{city}</b><br>
            <span style='color:#4caf50'>Rain Probability: {prob*100:.1f}%</span><br>
            <span style='font-size:11px;color:#90caf9'>June 2026 Prediction</span>
            </div>""",
            max_width=200
        ),
        tooltip=folium.Tooltip(f"{city}: {prob*100:.0f}%", sticky=True)
    ).add_to(m)
    
    folium.Marker(
        location=[lat + 0.4, lon],
        icon=folium.DivIcon(
            html=f'<div style="font-size:9px;color:white;background:{color};padding:2px 5px;border-radius:4px;white-space:nowrap;font-weight:bold">{city}<br>{prob*100:.0f}%</div>',
            icon_size=(65, 28),
            icon_anchor=(32, 0)
        )
    ).add_to(m)
    return m

def add_cloud_path(m, src_lat, src_lon, path_points, hottest_idx):
    # Cloud source
    folium.CircleMarker(
        location=[src_lat, src_lon],
        radius=16,
        color='#2196f3',
        fill=True, fill_color='#2196f3', fill_opacity=0.8,
        tooltip="☁️ Cloud Source",
        popup="Cloud Detection Point (Ocean)"
    ).add_to(m)
    
    coords = [[src_lat, src_lon]]
    for i, p in enumerate(path_points):
        is_burst = (i == hottest_idx)
        color = '#ff1744' if is_burst else '#ffab40'
        radius = 20 if is_burst else 10
        
        folium.CircleMarker(
            location=[p['lat'], p['lon']],
            radius=radius,
            color=color, fill=True,
           fill_color=color, fill_opacity=0.85,
tooltip=f"+{p['hours']}hrs | {p['temp']:.1f}C | {p['rain_prob']:.0f}%",
popup="RAIN BURST!" if is_burst else str(p['hours']) + "hrs point",
).add_to(m)
        coords.append([p['lat'], p['lon']])
    
    folium.PolyLine(
        coords, color='#4fc3f7',
        weight=2.5, opacity=0.8,
        dash_array='8 4'
    ).add_to(m)
    return m