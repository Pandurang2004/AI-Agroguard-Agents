from core.models import LLMClient

class VisionAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def analyze(self, crop: str, image_bytes: bytes, language: str = "English") -> str:
        prompt = f"""
You are an expert agricultural image analyst.

Analyze the provided image of {crop} crop leaves and describe:
1. Most likely pest/disease visible
2. Severity (Low/Medium/High)
3. Visible symptoms
4. Immediate treatment actions
5. Organic alternatives and dosages
6. Preventive actions for next 2–3 weeks

If quality is low or unclear, say what extra details are needed.

Respond in {language}.
"""
        return self.llm.generate_with_image(prompt, image_bytes)
