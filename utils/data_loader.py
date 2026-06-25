import pandas as pd
import numpy as np
import pickle
import os

# ============================================
# CITY PROFILES
# ============================================
CITY_PROFILES = {
    "Chennai":       {"lat": 13.08, "lon": 80.27, "zone": "coastal"},
    "Mumbai":        {"lat": 19.07, "lon": 72.87, "zone": "coastal"},
    "Delhi":         {"lat": 28.61, "lon": 77.20, "zone": "plains"},
    "Kolkata":       {"lat": 22.57, "lon": 88.36, "zone": "coastal"},
    "Bangalore":     {"lat": 12.97, "lon": 77.59, "zone": "plateau"},
    "Hyderabad":     {"lat": 17.38, "lon": 78.48, "zone": "plateau"},
    "Pune":          {"lat": 18.52, "lon": 73.85, "zone": "plateau"},
    "Ahmedabad":     {"lat": 23.02, "lon": 72.57, "zone": "plains"},
    "Jaipur":        {"lat": 26.91, "lon": 75.79, "zone": "desert"},
    "Lucknow":       {"lat": 26.85, "lon": 80.95, "zone": "plains"},
    "Kochi":         {"lat": 9.93,  "lon": 76.26, "zone": "coastal"},
    "Guwahati":      {"lat": 26.14, "lon": 91.74, "zone": "north_east"},
    "Bhopal":        {"lat": 23.25, "lon": 77.41, "zone": "plains"},
    "Nagpur":        {"lat": 21.14, "lon": 79.09, "zone": "plateau"},
    "Patna":         {"lat": 25.59, "lon": 85.13, "zone": "plains"},
    "Srinagar":      {"lat": 34.08, "lon": 74.79, "zone": "himalayan"},
    "Shimla":        {"lat": 31.10, "lon": 77.17, "zone": "himalayan"},
    "Bhubaneswar":   {"lat": 20.29, "lon": 85.82, "zone": "coastal"},
    "Visakhapatnam": {"lat": 17.68, "lon": 83.22, "zone": "coastal"},
    "Coimbatore":    {"lat": 11.02, "lon": 76.97, "zone": "plateau"},
}

# ============================================
# TRANSLATIONS
# ============================================
TRANSLATIONS = {
    "English": {
        "title": "Bharath Climate Twin",
        "subtitle": "AI-Powered 5-Layer Climate Intelligence System for India",
        "no_rain": "NO RAIN PREDICTED",
        "rain_predicted": "RAIN PREDICTED",
        "probability": "Probability",
        "flood_risk": "FLOOD RISK",
        "drought_risk": "DROUGHT RISK",
        "advisory": "Advisory",
        "predict_btn": "Predict Rain for 2026",
        "ask_ai": "Ask AI Assistant",
    },
    "தமிழ் (Tamil)": {
        "title": "பாரத் கிளைமேட் ட்வின்",
        "subtitle": "இந்தியாவிற்கான AI-இயங்கும் 5-அடுக்கு காலநிலை புலனாய்வு அமைப்பு",
        "no_rain": "மழை இல்லை",
        "rain_predicted": "மழை வரும்",
        "probability": "நிகழ்தகவு",
        "flood_risk": "வெள்ள ஆபத்து",
        "drought_risk": "வறட்சி ஆபத்து",
        "advisory": "ஆலோசனை",
        "predict_btn": "2026 மழையை கணிக்கவும்",
        "ask_ai": "AI உதவியாளரிடம் கேளுங்கள்",
    },
    "हिंदी (Hindi)": {
        "title": "भारत क्लाइमेट ट्विन",
        "subtitle": "भारत के लिए AI-संचालित 5-परत जलवायु बुद्धिमत्ता प्रणाली",
        "no_rain": "बारिश नहीं",
        "rain_predicted": "बारिश होगी",
        "probability": "संभावना",
        "flood_risk": "बाढ़ का खतरा",
        "drought_risk": "सूखे का खतरा",
        "advisory": "सलाह",
        "predict_btn": "2026 बारिश का अनुमान",
        "ask_ai": "AI सहायक से पूछें",
    },
    "తెలుగు (Telugu)": {
        "title": "భారత్ క్లైమేట్ ట్విన్",
        "subtitle": "భారతదేశం కోసం AI-ఆధారిత 5-పొర వాతావరణ నిఘా వ్యవస్థ",
        "no_rain": "వర్షం లేదు",
        "rain_predicted": "వర్షం వస్తుంది",
        "probability": "సంభావ్యత",
        "flood_risk": "వరద ప్రమాదం",
        "drought_risk": "కరువు ప్రమాదం",
        "advisory": "సలహా",
        "predict_btn": "2026 వర్షాన్ని అంచనా వేయండి",
        "ask_ai": "AI సహాయకుడిని అడగండి",
    },
    "മലയാളം (Malayalam)": {
        "title": "ഭാരത് ക്ലൈമേറ്റ് ട്വിൻ",
        "subtitle": "ഇന്ത്യയ്ക്കായുള്ള AI-പ്രവർത്തിത 5-പാളി കാലാവസ്ഥ ബുദ്ധി സംവിധാനം",
        "no_rain": "മഴ ഇല്ല",
        "rain_predicted": "മഴ വരും",
        "probability": "സാധ്യത",
        "flood_risk": "വെള്ളപ്പൊക്ക അപകടം",
        "drought_risk": "വരൾച്ച അപകടം",
        "advisory": "ഉപദേശം",
        "predict_btn": "2026 മഴ പ്രവചിക്കുക",
        "ask_ai": "AI സഹായകനോട് ചോദിക്കുക",
    },
}

def get_translation(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)

# ============================================
# PREDICT FUNCTION
# ============================================
def predict(model, lat, lon, tmax, tmin, month, year=2026):
    try:
        if model is None:
            # Fallback logic if no model
            base = 0.3
            if month in [6,7,8,9]:
                base += 0.35
            if lat < 15:
                base += 0.1
            if lon > 85:
                base += 0.05
            return min(base + np.random.normal(0, 0.05), 1.0)

        day_of_year = month * 30
        features = [[lat, lon, tmax, tmin, month, day_of_year]]
        prob = model.predict_proba(features)[0][1]
        return float(prob)
    except Exception as e:
        # Safe fallback
        base = 0.3
        if month in [6,7,8,9]:
            base += 0.3
        return min(base, 1.0)

# ============================================
# GET ADVISORY
# ============================================
def get_advisory(prob, zone="coastal", lang="English"):
    advisories = {
        "English": {
            "high_coastal":   "🌊 FLOOD ALERT: Coastal flooding likely. Evacuate low-lying areas. Fishermen — do not venture into sea.",
            "high_plains":    "🌧️ HEAVY RAIN: Waterlogging risk. Keep drains clear. Farmers — harvest ready crops NOW.",
            "high_plateau":   "⛈️ GOOD RAIN: Fill farm ponds. Activate rainwater harvesting. Good for Kharif crops.",
            "high_northeast": "🌊 FLOOD RISK: Brahmaputra/Barak levels rising. Activate disaster response.",
            "high_desert":    "💧 DRY SPELL: Rainfall below only in select areas. Groundwater conservation critical.",
            "high_himalayan": "🏔️ LANDSLIDE RISK: Mountain areas — stay indoors. Monitor cloud burst warnings.",
            "moderate":       "⛅ MODERATE: Normal farming activities. Monitor weekly updates.",
            "low_coastal":    "☀️ FAIR CONDITIONS: Normal farming. Check groundwater levels for irrigation.",
            "low_plains":     "☀️ DRY: Irrigation needed. Check soil moisture. Consider drought-resistant crops.",
            "low_desert":     "🏜️ VERY DRY: Extreme water conservation. Use drip irrigation only.",
        }
    }

    if prob > 0.6:
        key = f"high_{zone}" if f"high_{zone}" in advisories["English"] else "high_plains"
    elif prob > 0.35:
        key = "moderate"
    else:
        key = f"low_{zone}" if f"low_{zone}" in advisories["English"] else "low_plains"

    return advisories["English"].get(key, "Monitor local IMD updates.")

# ============================================
# GET CURRENT CONDITIONS
# ============================================
def get_current_conditions(lat, month):
    """Estimate current temperature based on location and month"""
    base_tmax = [29, 31, 34, 37, 39, 36, 32, 31, 32, 32, 30, 28]
    base_tmin = [18, 20, 23, 26, 28, 27, 25, 25, 24, 23, 21, 18]

    tmax = base_tmax[month - 1]
    tmin = base_tmin[month - 1]

    # Latitude adjustment
    lat_offset = (lat - 20) * 0.3
    tmax = tmax + lat_offset
    tmin = tmin + lat_offset * 0.8

    return round(tmax, 1), round(tmin, 1)

# ============================================
# LOAD FUNCTIONS
# ============================================
def load_climate_data():
    try:
        df = pd.read_csv('merged_climate_data.csv', low_memory=False)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['year']  = df['date'].dt.year
            df['month'] = df['date'].dt.month
        return df
    except Exception as e:
        try:
            df = pd.read_csv('rainfall_2021_2025.csv', low_memory=False)
            return df
        except:
            # Return empty dataframe with expected columns
            return pd.DataFrame(columns=['date','year','month','tmax','tmin','rainfall','lat','lon'])

def load_model():
    try:
        with open('rain_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except:
        return None

def load_groundwater():
    try:
        df = pd.read_csv('RS_Session_257_AU_2495_1.csv', low_memory=False)
        return df
    except:
        return None