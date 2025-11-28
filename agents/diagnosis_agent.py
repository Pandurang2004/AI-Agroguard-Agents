# agents/diagnosis_agent.py

from core.models import LLMClient

class DiagnosisAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(self, crop: str, symptoms: str) -> str:
        prompt = f"""
You are an agricultural plant disease expert.

Crop: {crop}
Observed symptoms: {symptoms}

1. Identify the most likely pest or disease.
2. Mention 1–2 alternative possibilities if unsure.
3. Specify how confident you are (High / Medium / Low).
4. Keep the answer concise but clear for a small farmer.
"""
        return self.llm.generate(prompt)
