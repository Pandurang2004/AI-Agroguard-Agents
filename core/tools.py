import requests
from datetime import datetime

def get_weather_summary(location: str) -> dict:
    try:
        # Normalize location to use only the city
        city = location.split(",")[0].strip()

        # Step 1: Geocode search
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_response = requests.get(geo_url).json()

        if "results" not in geo_response or not geo_response["results"]:
            raise ValueError("Location not found")

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        # Step 2: Fetch weather data
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,precipitation_probability"
        )

        weather_response = requests.get(weather_url).json()

        temp = weather_response["hourly"]["temperature_2m"][0]
        humidity = weather_response["hourly"]["relative_humidity_2m"][0]
        rain = weather_response["hourly"]["precipitation_probability"][0]

        summary = "Warm conditions with rain expected" if rain > 40 else "Dry moderate weather"

        return {
            "location": location,
            "latitude": lat,
            "longitude": lon,
            "temperature_c": temp,
            "humidity": humidity,
            "rain_chance": rain,
            "summary": summary,
            "date": datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {
            "error": str(e),
            "location": location,
            "temperature_c": 28,
            "humidity": 60,
            "rain_chance": 20,
            "summary": "Fallback weather data due to API error"
        }
