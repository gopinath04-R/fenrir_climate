import numpy as np
from datetime import datetime

CITY_PROFILES = {
    'chennai': {'lat': 13.08, 'lon': 80.27, 'state': 'Tamil Nadu', 'zone': 'coastal'},
    'mumbai': {'lat': 19.07, 'lon': 72.87, 'state': 'Maharashtra', 'zone': 'coastal'},
    'delhi': {'lat': 28.61, 'lon': 77.21, 'state': 'Delhi', 'zone': 'plains'},
    'kolkata': {'lat': 22.57, 'lon': 88.36, 'state': 'West Bengal', 'zone': 'coastal'},
    'bengaluru': {'lat': 12.97, 'lon': 77.59, 'state': 'Karnataka', 'zone': 'plateau'},
    'hyderabad': {'lat': 17.38, 'lon': 78.47, 'state': 'Telangana', 'zone': 'plateau'},
    'kochi': {'lat': 9.93, 'lon': 76.26, 'state': 'Kerala', 'zone': 'coastal'},
    'jaisalmer': {'lat': 26.91, 'lon': 70.90, 'state': 'Rajasthan', 'zone': 'desert'},
    'pune': {'lat': 18.52, 'lon': 73.86, 'state': 'Maharashtra', 'zone': 'plateau'},
    'guwahati': {'lat': 26.14, 'lon': 91.74, 'state': 'Assam', 'zone': 'northeast'},
}

def get_advisory(prob, zone, lang='English'):
    advisories = {
        'English': {
            'high_coastal': "🌊 FLOOD ALERT: Coastal flooding likely. Evacuate low-lying areas. Fishermen — do not venture into sea.",
            'high_plains': "🌧️ HEAVY RAIN: Waterlogging risk. Farmers — harvest ready crops. Drain agricultural fields.",
            'high_plateau': "🌧️ GOOD RAIN: Excellent for reservoir filling. Farmers — sow Kharif crops now.",
            'high_desert': "💧 RARE RAIN: Collect every drop! Activate rainwater harvesting. Store in tanks.",
            'high_northeast': "🌊 FLOOD RISK: Brahmaputra/Barak levels rising. Activate disaster response.",
            'low_coastal': "☀️ DRY SPELL: Activate desalination/water conservation. Monitor groundwater.",
            'low_desert': "🏜️ SEVERE DROUGHT: Plant Bajra/Moth bean only. MGNREGA water conservation.",
            'low_plains': "⚠️ DROUGHT RISK: Irrigation from canals essential. Crop insurance recommended.",
            'moderate': "🌤️ MODERATE CONDITIONS: Normal farming activities. Monitor weekly updates.",
        },
        'தமிழ் (Tamil)': {
            'high_coastal': "🌊 வெள்ள எச்சரிக்கை: கடலோர பகுதிகளை காலி செய்யுங்கள். மீனவர்கள் கடலுக்கு செல்லாதீர்கள்.",
            'high_plateau': "🌧️ நல்ல மழை: கரீஃப் பயிர்கள் விதைக்க சிறந்த நேரம். நீர்த்தேக்கங்கள் நிரம்பும்.",
            'low_desert': "🏜️ கடும் வறட்சி: கம்பு, முதிரை மட்டும் சாகுபடி செய்யுங்கள்.",
            'moderate': "🌤️ சாதாரண நிலை: வழக்கமான விவசாய பணிகள் தொடரலாம்.",
        }
    }
    
    lang_advisories = advisories.get(lang, advisories['English'])
    
    if prob > 0.65:
        key = f'high_{zone}'
        return lang_advisories.get(key, lang_advisories.get('high_plains', ''))
    elif prob < 0.35:
        key = f'low_{zone}'
        return lang_advisories.get(key, lang_advisories.get('low_plains', ''))
    else:
        return lang_advisories.get('moderate', '')

def predict(model, lat, lon, tmax, tmin, month):
    if not model:
        return None, None
    doy = datetime(2026, month, 15).timetuple().tm_yday
    pred = model.predict([[lat, lon, tmax, tmin, month, doy]])[0]
    prob = model.predict_proba([[lat, lon, tmax, tmin, month, doy]])[0][1]
    return pred, prob

def get_current_conditions(lat, month):
    """Estimate current temperature based on lat and month"""
    base_temp = 25 + (20 - lat) * 0.4
    seasonal = [0, -2, 1, 4, 7, 8, 6, 5, 4, 2, -1, -2][month - 1]
    tmax = round(base_temp + seasonal + 5, 1)
    tmin = round(base_temp + seasonal - 3, 1)
    return tmax, tmin