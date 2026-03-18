# ~/core/kernel/agents/gemini.py
from google import genai

class GeminiAgent:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        print(f"GeminiAgent.generate called with prompt: {prompt}")
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            print(f"GeminiAgent.generate response: {response}")
            return response.text
        except Exception as e:
            print(f"GeminiAgent.generate error: {e}")
            raise
