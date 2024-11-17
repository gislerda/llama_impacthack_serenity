from .base_agent import BaseAgent
from typing import Dict
 # Read events from JSON file
import json
import os

class CopingAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct path to events.json (assuming it's in the bot/data directory)
        events_path = os.path.join(current_dir, "..","..","data", "copingstrategies.json")
        
        # Read and load events
        with open(events_path, 'r') as f:
            events = json.load(f)
            
        # Convert events to formatted string for prompt
        events_str = json.dumps(events, indent=2)
        
        self.system_prompt = f"""
        You are a coping strategy suggestion assistant. Below is a list of available coping strategies:

        {events_str}

        Suggest a cool event from this list that might interest the user. Format your response as a friendly suggestion.
        """

    async def process_message(self,  user_message: str,  user_id: int) -> str:
        try:
            print(f"COPING: {self.system_prompt}")
            message = f"user_message: {user_message}"
            response = self.get_ai_response(message)
            return response
        except Exception as e:
            print(f"Error in conversation agent: {e}")
            return "I'm having trouble processing that right now. Could you try rephrasing your message?"