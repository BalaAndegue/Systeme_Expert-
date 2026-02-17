import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import time

# Cache simple pour éviter appels répétés (TTL: 15 minutes)
_weather_cache = {}
_cache_ttl = 900  # 15 minutes en secondes

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

# Données climatiques de fallback par région
FALLBACK_CLIMATE_DATA = {
    "Centre": {"temp_avg": 24, "rainfall_annual": 1600, "climate": "Équatorial"},
    "Littoral": {"temp_avg": 26, "rainfall_annual": 4000, "climate": "Équatorial côtier"},
    "Ouest": {"temp_avg": 20, "rainfall_annual": 2000, "climate": "Tropical d'altitude"},
    "Nord-Ouest": {"temp_avg": 22, "rainfall_annual": 2500, "climate": "Tropical d'altitude"},
    "Sud-Ouest": {"temp_avg": 25, "rainfall_annual": 4000, "climate": "Équatorial"},
    "Sud": {"temp_avg": 24, "rainfall_annual": 1500, "climate": "Équatorial"},
    "Est": {"lat": 24, "rainfall_annual": 1500, "climate": "Équatorial"},
    "Adamaoua": {"temp_avg": 22, "rainfall_annual": 1500, "climate": "Tropical soudanien"},
    "Nord": {"temp_avg": 28, "rainfall_annual": 900, "climate": "Soudano-sahélien"},
    "Extrême-Nord": {"temp_avg": 28, "rainfall_annual": 600, "climate": "Sahélien"},
}


def _get_cache_key(region_name: str, data_type: str) -> str:
    """Génère une clé de cache."""
    return f"{region_name}_{data_type}"


def _is_cache_valid(cache_key: str) -> bool:
    """Vérifie si le cache est encore valide."""
    if cache_key not in _weather_cache:
        return False
    cached_time = _weather_cache[cache_key].get('_cached_at', 0)
    return (time.time() - cached_time) < _cache_ttl


def fetch_weather_data(region_name: str, daily: bool = False) -> Optional[Dict[str, Any]]:
    """
    Récupère les données météo pour une région via Open-Meteo API.
    Utilise un cache de 15 minutes pour éviter les appels répétés.
    """
    cache_key = _get_cache_key(region_name, "daily" if daily else "current")
    
    # Vérifier le cache
    if _is_cache_valid(cache_key):
        return _weather_cache[cache_key]['data']
    
    coords = REGION_COORDINATES.get(region_name)
    if not coords:
        print(f"Région inconnue: {region_name}")
        return None
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true"
        if daily:
            url += "&daily=precipitation_sum,temperature_2m_max,temperature_2m_min,et0_fao_evapotranspiration,windspeed_10m_max&timezone=auto&forecast_days=14"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Mise en cache
        _weather_cache[cache_key] = {
            'data': data,
            '_cached_at': time.time()
        }
        
        return data
        
    except requests.exceptions.Timeout:
        print(f"Timeout lors de la récupération météo pour {region_name}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Erreur de connexion à l'API météo pour {region_name}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP {e.response.status_code} pour {region_name}")
        return None
    except Exception as e:
        print(f"Erreur inattendue lors de la récupération météo: {e}")
        return None


def get_weather_forecast(region_name: str) -> str:
    """Obtient les prévisions à 3, 7 et 14 jours de manière concise."""
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'daily' not in data:
        return "❌ Prévisions indisponibles."
    
    daily = data['daily']
    forecasts = []
    for days in [3, 7, 14]:
        idx = days - 1
        if idx < len(daily['time']):
            date = daily['time'][idx]
            tmax = daily['temperature_2m_max'][idx]
            tmin = daily['temperature_2m_min'][idx]
            precip = daily['precipitation_sum'][idx]
            forecasts.append(f"J+{days}: {tmin:.0f}-{tmax:.0f}°C, {precip:.1f}mm")
    
    return "\n".join(forecasts) if forecasts else "Données insuffisantes"


def get_irrigation_advice(region_name: str) -> str:
    """Conseils d'irrigation basés sur précipitations et évapotranspiration."""
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'daily' not in data:
        fallback = FALLBACK_CLIMATE_DATA.get(region_name, {})
        rainfall = fallback.get('rainfall_annual', 1500)
        if rainfall < 1000:
            return "⚠️ Zone à faible pluviométrie. Irrigation fortement recommandée."
        return "ℹ️ Données temps réel indisponibles. Suivez calendrier local."
    
    daily = data['daily']
    total_precip = sum(daily['precipitation_sum'][:3])
    total_et0 = sum(daily['et0_fao_evapotranspiration'][:3])
    
    if total_precip < total_et0 * 0.5:
        deficit = total_et0 - total_precip
        return f"🚰 IRRIGATION NÉCESSAIRE. Déficit: {deficit:.1f}mm sur 3j. Arroser tôt le matin."
    elif total_precip < total_et0:
        return f"⚡ Irrigation modérée conseillée. Précip: {total_precip:.1f}mm, ET0: {total_et0:.1f}mm."
    else:
        return f"✅ Irrigation non nécessaire. Précipitations suffisantes: {total_precip:.1f}mm."


def get_climate_alerts(region_name: str) -> str:
    """Détecte conditions météo dangereuses pour agriculture."""
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'current_weather' not in data:
        return "ℹ️ Surveillance météo indisponible."
    
    current = data['current_weather']
    wind = current.get('windspeed', 0)
    
    alerts = []
    if wind > 40:
        alerts.append(f"🌪️ ALERTE VENT: {wind:.0f} km/h. Protégez cultures fragiles.")
    
    if 'daily' in data:
        daily = data['daily']
        next_3d_rain = sum(daily['precipitation_sum'][:3])
        if next_3d_rain > 100:
            alerts.append(f"⛈️ ALERTE PLUIE: {next_3d_rain:.0f}mm prévus. Risque inondation/érosion.")
        elif next_3d_rain > 50:
            alerts.append(f"🌧️ Fortes pluies: {next_3d_rain:.0f}mm. Drainage requis.")
        
        # Vérifier vents violents prévus
        if 'windspeed_10m_max' in daily:
            max_wind = max(daily['windspeed_10m_max'][:3])
            if max_wind > 50:
                alerts.append(f"💨 Vents violents prévus: {max_wind:.0f} km/h.")
    
    return "\n".join(alerts) if alerts else "✅ Aucune alerte météo."


def analyze_rainfall_patterns(region_name: str) -> str:
    """Analyse tendances pluviométriques sur 14 jours."""
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'daily' not in data:
        return "Analyse pluviométrique indisponible."
    
    precip_list = data['daily']['precipitation_sum']
    rainy_days = len([p for p in precip_list if p > 0.5])
    total_rain = sum(precip_list)
    avg_rain = total_rain / len(precip_list) if precip_list else 0
    
    if total_rain < 10:
        pattern = "SEC 🌵"
        advice = "Prévoir irrigation intensive."
    elif total_rain > 100:
        pattern = "TRÈS HUMIDE 🌊"
        advice = "Attention drainage et maladies fongiques."
    elif total_rain > 50:
        pattern = "HUMIDE 💧"
        advice = "Bonnes conditions. Surveiller excès d'eau."
    else:
        pattern = "MODÉRÉ 🌤️"
        advice = "Conditions favorables."
    
    return f"{pattern} | Total 14j: {total_rain:.0f}mm ({rainy_days}j pluie) | {advice}"


def get_agricultural_weather_summary(region_name: str) -> str:
    """
    Synthèse météo agricole concise combinant conditions actuelles et prévisions.
    """
    current_data = fetch_weather_data(region_name, daily=False)
    daily_data = fetch_weather_data(region_name, daily=True)
    
    if not current_data or 'current_weather' not in current_data:
        fallback = FALLBACK_CLIMATE_DATA.get(region_name, {})
        return f"📍 {region_name}: Données temps réel indisponibles. Climat: {fallback.get('climate', 'N/A')}"
    
    current = current_data['current_weather']
    temp = current.get('temperature', 0)
    wind = current.get('windspeed', 0)
    
    summary = f"🌡️ Actuellement: {temp:.1f}°C, Vent: {wind:.0f}km/h"
    
    if daily_data and 'daily' in daily_data:
        daily = daily_data['daily']
        next_3d = sum(daily['precipitation_sum'][:3])
        summary += f"\n💧 Pluie 3j: {next_3d:.0f}mm"
    
    return summary


def get_frost_risk(region_name: str) -> str:
    """
    Évalue risque de gel pour régions montagneuses (Ouest, Nord-Ouest, Adamaoua).
    """
    mountain_regions = ["Ouest", "Nord-Ouest", "Adamaoua"]
    
    if region_name not in mountain_regions:
        return "ℹ️ Risque de gel non pertinent pour cette région."
    
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'daily' not in data:
        return "⚠️ Évaluation risque gel indisponible."
    
    daily = data['daily']
    min_temps = daily['temperature_2m_min'][:7]  # 7 prochains jours
    
    critical_temps = [t for t in min_temps if t < 5]
    frost_temps = [t for t in min_temps if t < 0]
    
    if frost_temps:
        min_temp = min(frost_temps)
        return f"❄️ ALERTE GEL: {min_temp:.1f}°C prévu. Protégez cultures sensibles!"
    elif critical_temps:
        min_temp = min(critical_temps)
        return f"⚠️ Températures basses: {min_temp:.1f}°C. Surveillez cultures."
    else:
        min_temp = min(min_temps)
        return f"✅ Pas de risque gel. Minimum: {min_temp:.1f}°C."


def get_optimal_planting_conditions(region_name: str, crop_type: str = "général") -> str:
    """
    Évalue si conditions actuelles sont optimales pour plantation.
    """
    data = fetch_weather_data(region_name, daily=True)
    if not data or 'daily' not in data:
        return "⚠️ Évaluation conditions plantation indisponible."
    
    daily = data['daily']
    next_7d_rain = sum(daily['precipitation_sum'][:7])
    next_7d_temps = daily['temperature_2m_max'][:7]
    avg_temp = sum(next_7d_temps) / len(next_7d_temps) if next_7d_temps else 0
    
    conditions = []
    score = 0
    
    # Critère pluie (idéal: 20-50mm sur 7j pour début)
    if 20 <= next_7d_rain <= 50:
        conditions.append("✅ Pluie optimale")
        score += 2
    elif 10 <= next_7d_rain < 20 or 50 < next_7d_rain <= 80:
        conditions.append("⚡ Pluie acceptable")
        score += 1
    else:
        conditions.append(f"❌ Pluie non optimale ({next_7d_rain:.0f}mm)")
    
    # Critère température (idéal: 20-30°C pour plupart cultures)
    if 20 <= avg_temp <= 30:
        conditions.append("✅ Température idéale")
        score += 2
    elif 15 <= avg_temp < 20 or 30 < avg_temp <= 35:
        conditions.append("⚡ Température acceptable")
        score += 1
    else:
        conditions.append(f"❌ Température non optimale ({avg_temp:.0f}°C)")
    
    # Verdict
    if score >= 3:
        verdict = "🌱 CONDITIONS EXCELLENTES pour plantation"
    elif score >= 2:
        verdict = "✅ Conditions favorables"
    else:
        verdict = "⚠️ Conditions sous-optimales. Attendre amélioration."
    
    return f"{verdict}\n" + " | ".join(conditions)


def format_weather_data(data: Dict[str, Any]) -> str:
    """Formate données météo actuelles de manière concise."""
    if not data or 'current_weather' not in data:
        return "Données indisponibles"
    
    current = data['current_weather']
    temp = current.get('temperature', 'N/A')
    wind = current.get('windspeed', 'N/A')
    
    return f"{temp}°C, vent {wind}km/h"
