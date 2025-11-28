# agents/recommendation_agent.py

from core.models import LLMClient

class RecommendationAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, crop: str, diagnosis_summary: str) -> str:
        prompt = f"""
You are an agricultural advisory assistant.

Given:
Crop: {crop}
Diagnosis Summary:
{diagnosis_summary}

Provide:
1. Immediate treatment steps (simple bullet points).
2. Suggested pesticide type and dosage range, with safety warnings.
3. Organic or low-chemical alternative if possible.
4. Preventive measures for the next 2–3 weeks.

Use simple language suitable for smallholder farmers.
"""
        return self.llm.generate(prompt)
