# agents/diagnosis_agent.py

from core.models import LLMClient
from typing import Optional


class DiagnosisAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def run(
        self,
        crop: str,
        symptoms: str,
        language: str = "English",
        image_bytes: Optional[bytes] = None,
    ) -> str:
        prompt = f"""
You are an agricultural plant disease expert.

Crop: {crop}
Observed symptoms (farmer description): {symptoms}

If an image is provided, carefully analyze visible leaf / stem patterns, colors, spots, pests, or damage.

Tasks:
1. Identify the most likely pest or disease.
2. Mention 1–2 alternative possibilities if unsure.
3. Specify how confident you are (High / Medium / Low).
4. Explain the reasoning in simple terms suitable for rural farmers.

Respond in {language}. Use short, simple sentences.
"""

        if image_bytes:
            return self.llm.generate_with_image(prompt, image_bytes)
        else:
            return self.llm.generate(prompt)
