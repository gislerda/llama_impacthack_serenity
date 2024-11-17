from .base_agent import BaseAgent
from typing import Dict
 # Read events from JSON file
import json
import os

class CheckinAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        # Get the directory of the current file        
        # Read and load events
        
        self.system_prompt = f"""
        You are a compassionate AI companion focused on helping people feel less lonely. 
        Your responses should be:
        - Empathetic and understanding
        - Encouraging but realistic
        - Focused on the user's emotional well-being
        - Natural and conversational

        Your Task is to ask a follow-up question on whether the user enjoyed going to the in a previous user-message. Make it like small talk and ask what they enjoyed for example.
        Keep the message BRIEF. one sentence max.
        """

    async def process_message(self,  user_message: str,  user_id: int, context: str) -> str:
        try:
            print(f"Events: {self.system_prompt}")
            self.system_prompt += f" YOU HAVE FURTHER CONTEXT FOR ANSWERING, DO NOT REFERENCE THIS CONTEXT BUT MAKE USE OF IT: {context}"
            message = f"user_message: {user_message}"
            response = self.get_ai_response(message)
            return response
        except Exception as e:
            print(f"Error in conversation agent: {e}")
            return "I'm having trouble processing that right now. Could you try rephrasing your message?"