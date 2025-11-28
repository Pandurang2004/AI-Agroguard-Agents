# core/tools.py

import requests
from datetime import datetime

def get_weather_summary(location: str) -> dict:
    """
    Tool: fetch or simulate weather for given location.
    You can integrate Open-Meteo / OpenWeather here.
    For now, we return a mock response structure.
    """
    # TODO: integrate real API
    # Example minimal mock:
    return {
        "location": location,
        "date": datetime.utcnow().isoformat(),
        "temperature_c": 28,
        "humidity": 70,
        "rain_chance": 60,
        "summary": "Warm, humid, moderate chance of rain"
    }
