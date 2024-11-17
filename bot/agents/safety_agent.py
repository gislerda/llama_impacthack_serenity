from groq import Groq
from typing import Dict
from config import GROQ_API_KEY

class SafetyAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-guard-3-8b"

    async def check_message(self, message: str) -> Dict:
        """
        Check a message for safety concerns using Llama-Guard
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }                    
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            # Collect the streamed response
            full_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content

            # Analyze the response
            is_unsafe = "unsafe" in full_response.lower()
            
            return {
                "is_safe": not is_unsafe,
                "analysis": full_response,
                "original_message": message
            }
            
        except Exception as e:
            print(f"Error in safety check: {e}")
            return {
                "is_safe": False,  # Err on the side of caution
                "analysis": f"Error occurred during safety assessment: {str(e)}",
                "original_message": message
            }