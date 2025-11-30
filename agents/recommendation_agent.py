# agents/recommendation_agent.py

from typing import List, Dict, Any, Optional
from core.models import LLMClient


class RecommendationAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(
        self,
        crop: str,
        diagnosis_summary: str,
        language: str = "English",
        history: Optional[List[Dict[str, Any]]] = None,
        farmer_trend_text: Optional[str] = None,
        local_trend_text: Optional[str] = None,
    ) -> str:

        if history:
            last_cases = history[-5:]
            simple_history = "\n".join(
                [
                    f"- {h.get('timestamp','')}: {h.get('crop','')} at {h.get('location','')} — risk {h.get('risk_level','')}"
                    for h in last_cases
                ]
            )
        else:
            simple_history = "No previous cases for this farmer."

        farmer_trend_text = farmer_trend_text or "No long-term trends available."
        local_trend_text = local_trend_text or "No local region data available."

        prompt = f"""
You are an agricultural advisory expert.

Crop: {crop}

Current diagnosis summary:
{diagnosis_summary}

Farmer recent history:
{simple_history}

Farmer trend summary:
{farmer_trend_text}

Local crop-location trend summary:
{local_trend_text}

Use trends to adapt recommendations:
- Emphasize stronger action if high risk is frequent.
- Encourage lightly if improving trend.
- Suggest crop rotation or resistant seeds if repeated disease.
- Warn if region has many cases.
- Provide emotional support tone.

Now provide:
1. Short immediate action steps.
2. Pesticide type + dosage + safety notes.
3. Organic alternatives.
4. Prevention plan for 2–3 weeks referencing history patterns.
5. A motivational closing line.

Respond in {language}.
"""
        return self.llm.generate(prompt)
