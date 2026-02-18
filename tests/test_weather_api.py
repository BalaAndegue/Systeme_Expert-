import pytest
from app.agents.weather.tools import fetch_weather_data, format_weather_data

def test_fetch_weather_data_centre():
    data = fetch_weather_data("Centre")
    assert data is not None
    assert "current_weather" in data
    assert "temperature" in data["current_weather"]

def test_fetch_weather_data_invalid():
    data = fetch_weather_data("Inconnu")
    assert data is None

def test_format_weather_data():
    mock_data = {
        "current_weather": {
            "temperature": 25.5,
            "windspeed": 10.2
        }
    }
    formatted = format_weather_data(mock_data)
    assert "25.5°C" in formatted
    assert "10.2km/h" in formatted

def test_format_weather_data_none():
    formatted = format_weather_data(None)
    assert "indisponibles" in formatted.lower() or "indisponible" in formatted.lower()
