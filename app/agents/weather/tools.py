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

def fetch_weather_data(region_name: str) -> Dict[str, Any]:
    """Récupère la météo actuelle pour une région via Open-Meteo API."""
    coords = REGION_COORDINATES.get(region_name)
    if not coords:
        return None
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur lors de la récupération de la météo: {e}")
        return None

def format_weather_data(data: Dict[str, Any]) -> str:
    """Formate les données météo pour le prompt."""
    if not data or 'current_weather' not in data:
        return "Données météo non disponibles temporairement."
    
    current = data['current_weather']
    temp = current.get('temperature')
    windspeed = current.get('windspeed')
    
    return f"Température: {temp}°C, Vitesse du vent: {windspeed} km/h."
