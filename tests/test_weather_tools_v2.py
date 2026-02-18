import pytest
from app.agents.weather.tools import (
    get_weather_forecast, 
    get_irrigation_advice, 
    get_climate_alerts, 
    analyze_rainfall_patterns
)

def test_weather_forecast():
    forecast = get_weather_forecast("Centre")
    assert "J+3" in forecast
    assert "J+7" in forecast
    assert "J+14" in forecast
    assert "mm" in forecast  # précipitations en mm

def test_irrigation_advice():
    advice = get_irrigation_advice("Centre")
    # Vérifie que la réponse contient des informations d'irrigation
    assert any(word in advice for word in ["IRRIGATION", "Irrigation", "irrigation", "Précip", "suffisantes", "conseillée"])

def test_climate_alerts():
    alerts = get_climate_alerts("Centre")
    assert "alerte" in alerts.lower()

def test_rainfall_patterns():
    patterns = analyze_rainfall_patterns("Centre")
    # Vérifie que la réponse contient des données pluviométriques
    assert "mm" in patterns or "indisponible" in patterns.lower()
