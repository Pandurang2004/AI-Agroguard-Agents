# core/models.py

import os

# TODO: Integrate actual Gemini / LLM SDK here.
# For now, mock with simple string formatting or a placeholder.

class LLMClient:
    def __init__(self):
        # Example: load API key from env
        self.model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")

    def generate(self, prompt: str) -> str:
        """
        Central place to call your LLM.
        Replace this body with actual Gemini / ADK call.
        """
        # TODO: Replace with real LLM call
        return f"[MOCKED LLM RESPONSE]\nPrompt was:\n{prompt[:500]}"
