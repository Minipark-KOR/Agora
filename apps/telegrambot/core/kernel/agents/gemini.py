
import logging
from google import genai

logger = logging.getLogger(__name__)

class GeminiAgent:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        logger.debug(f"GeminiAgent.generate called with prompt: {prompt}")
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            logger.debug(f"GeminiAgent.generate response: {response}")
            return response.text
        except Exception as e:
            logger.error(f"GeminiAgent.generate error: {e}", exc_info=True)
            raise
