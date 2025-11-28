# agents/weather_risk_agent.py

from core.models import LLMClient
from core.tools import get_weather_summary

class WeatherRiskAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, crop: str, location: str, diagnosis_summary: str) -> tuple[str, dict]:
        weather = get_weather_summary(location)

        prompt = f"""
You are an agricultural risk analyst.

Crop: {crop}
Location: {location}
Diagnosis Summary:
{diagnosis_summary}

Weather data:
- Temperature (C): {weather['temperature_c']}
- Humidity (%): {weather['humidity']}
- Chance of Rain (%): {weather['rain_chance']}
- Summary: {weather['summary']}

Tasks:
1. Estimate pest/disease risk level for the upcoming 7 days
   (Low / Medium / High) with 1–2 lines of reasoning.
2. Suggest if the farmer should intensify monitoring or treatment.

Format:
Risk Level: <Low/Medium/High>
Reason: <one line>
Advice: <one or two lines>
"""
        risk_analysis = self.llm.generate(prompt)

        # You can parse risk level from the response later; for now, just return whole text.
        return risk_analysis, weather
