from .base_agent import BaseAgent
from typing import Dict
 # Read events from JSON file
import json
import os

class ModeratorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        
        
        self.system_prompt = f"""
        You are a moderation suggestion assistant. You moderate potentially unsafe prompts on self-harm and formulate them in a safe way as much as possible.
        - Make sure your message intends no harm and has no unintended consequences.
        - You can relate and reference self-harm and suicide. However, treat the topic with delicacy.
        - Always argue positively and try to emphatize with the topic but firmly push for a "good outcom"
        """

    async def process_message(self,  user_message: str,  user_id: int) -> str:
        try:
            print(f"MODERATION: {self.system_prompt}")
            message = f"user_message: {user_message}"
            response = self.get_ai_response(message)
            return response
        except Exception as e:
            print(f"Error in Moderator agent: {e}")
            return "There was an error in Moderation."