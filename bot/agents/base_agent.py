from abc import ABC, abstractmethod
import groq
from config import GROQ_API_KEY

class BaseAgent(ABC):
    def __init__(self):
        self.client = groq.Client(api_key=GROQ_API_KEY)
        self.model = "llama-3.2-11b-vision-preview"
        self.system_prompt = "You are a base class. If you are prompted, you respond with sorry, i cant help with that."
        self.tool_choice = "auto"
        self.tools = None

    @abstractmethod
    async def process_message(self, message: str, user_id: int):
        pass
    
    def get_ai_response(self, prompt: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}],
                model=self.model,tools=self.tools,tool_choice=self.tool_choice
            )
            #print(f"Debug: {chat_completion.choices[0]}")
            choice = chat_completion.choices[0]
            if choice.finish_reason == "tool_calls":
                return choice.message
            else:
                return choice.message.content
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return "I'm having trouble right now. Could you try again in a moment?"