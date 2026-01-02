import requests
from typing import Dict, Any

REGION_COORDINATES = {
    "Centre": {"lat": 3.8480, "lon": 11.5021},
    "Littoral": {"lat": 4.0511, "lon": 9.7679},
    "Ouest": {"lat": 5.4777, "lon": 10.4176},
    "Nord-Ouest": {"lat": 5.9631, "lon": 10.1591},
    "Sud-Ouest": {"lat": 4.1500, "lon": 9.2333},
    "Sud": {"lat": 2.9167, "lon": 11.1500},
    "Est": {"lat": 4.5833, "lon": 13.6833},
    "Adamaoua": {"lat": 7.3167, "lon": 13.5833},
    "Nord": {"lat": 9.3000, "lon": 13.4000},
    "Extrême-Nord": {"lat": 10.5972, "lon": 14.3158},
}

def fetch_weather_data(region_name: str, daily: bool = False) -> Dict[str, Any]:
    """Récupère les données météo pour une région via Open-Meteo API."""
    coords = REGION_COORDINATES.get(region_name)
    if not coords:
        return None
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true"
        if daily:
            url += "&daily=precipitation_sum,temperature_2m_max,temperature_2m_min,et0_fao_evapotranspiration&timezone=auto&forecast_days=14"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur lors de la récupération de la météo: {e}")
        return None

def get_weather_forecast(region_name: str) -> str:
    """Obtient les prévisions à 3, 7 et 14 jours."""
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'daily' not in data:
        return "Prévisions non disponibles."
    
    daily = data['daily']
    forecasts = []
    for days in [3, 7, 14]:
        idx = days - 1
        if idx < len(daily['time']):
            date = daily['time'][idx]
            tmax = daily['temperature_2m_max'][idx]
            tmin = daily['temperature_2m_min'][idx]
            precip = daily['precipitation_sum'][idx]
            forecasts.append(f"J+{days} ({date}): {tmin}°C - {tmax}°C, Pluie: {precip}mm")
    
    return "\n".join(forecasts)

def get_irrigation_advice(region_name: str) -> str:
    """Donne des conseils d'irrigation basés sur les précipitations récentes et l'évapotranspiration."""
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'daily' not in data:
        return "Données pour l'irrigation non disponibles."
    
    daily = data['daily']
    total_precip = sum(daily['precipitation_sum'][:3])  # 3 derniers jours (simulés par les 3 premiers jours du forecast ici)
    total_et0 = sum(daily['et0_fao_evapotranspiration'][:3])
    
    if total_precip < total_et0:
        return f"Conseil: Irrigation nécessaire. Précipitations (3j): {total_precip:.1f}mm vs Évapotranspiration: {total_et0:.1f}mm. Arrosage recommandé tôt le matin."
    else:
        return f"Conseil: Irrigation non prioritaire. Précipitations suffisantes ({total_precip:.1f}mm)."

def get_climate_alerts(region_name: str) -> str:
    """Détecte les conditions dangereuses."""
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'current_weather' not in data:
        return "Aucune alerte disponible."
    
    current = data['current_weather']
    wind = current.get('windspeed', 0)
    
    alerts = []
    if wind > 40:
        alerts.append(f"ALERTE: Vents violents détectés ({wind} km/h).")
    
    daily = data['daily']
    next_3d_rain = sum(daily['precipitation_sum'][:3])
    if next_3d_rain > 50:
        alerts.append(f"ALERTE: Fortes pluies prévues (total 50mm+ sur 3 jours). Risque d'inondation.")
        
    return "\n".join(alerts) if alerts else "Aucune alerte majeure identifiée."

def analyze_rainfall_patterns(region_name: str) -> str:
    """Analyse les tendances de pluie sur 14 jours."""
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'daily' not in data:
        return "Analyse impossible."
    
    precip_list = data['daily']['precipitation_sum']
    rainy_days = len([p for p in precip_list if p > 0.5])
    total_rain = sum(precip_list)
    
    pattern = "sec" if total_rain < 10 else "humide" if total_rain > 50 else "modéré"
    return f"Tendance 14 jours: Cycle {pattern}. Total prévu: {total_rain:.1f}mm sur {rainy_days} jours de pluie."

def format_weather_data(data: Dict[str, Any]) -> str:
    """Formate les données météo actuelles."""
    if not data or 'current_weather' not in data:
        return "Données météo non disponibles temporairement."
    
    current = data['current_weather']
    temp = current.get('temperature')
    windspeed = current.get('windspeed')
    
    return f"Température: {temp}°C, Vitesse du vent: {windspeed} km/h."
