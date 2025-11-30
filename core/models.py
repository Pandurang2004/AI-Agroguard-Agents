# core/models.py

import os
import io
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()


class LLMClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY in .env file")
        genai.configure(api_key=api_key)
        # Text + vision capable model
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[ERROR calling Gemini API]: {e}"

    def generate_with_image(self, prompt: str, image_bytes: bytes) -> str:
        try:
            img = Image.open(io.BytesIO(image_bytes))
            response = self.model.generate_content([prompt, img])
            return response.text
        except Exception as e:
            return f"[ERROR calling Gemini Vision]: {e}"
