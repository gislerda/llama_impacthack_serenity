from bot.agents.base_agent import BaseAgent
from typing import Dict
from ..database.database import store_memory, get_memories, get_important_memories

class ConversationAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = """
        You are a compassionate AI companion focused on helping people feel less lonely. 
        Your responses should be:
        - Empathetic and understanding
        - Encouraging but realistic
        - Focused on the user's emotional well-being
        - Natural and conversational

        You are receiving enriched context pieces:
        - nhs_message
        - safety_check
        - added_context
        - user_message
        - sentiment history
        - (optional) Image_description

        Formulate a response to "user_message" that is appropriate. 
        Use the other context pieces to enhance the response message. Do not reference the existence of these additional context pieces.

        IF YOU FEEL A SIGNIFICANT DROP IN SENTIMENT; ASK WHETHER THE USER WOULD LIKE TO SHARE THE REASON OR IF SOMETHING HAPPENED
        """
        #TODO: Remove - Deprecated


    async def process_message(self, nhs_message: str, safetey_check: Dict, user_message: str, added_context: str, user_id: int) -> str:
        try:
            prompt = f"nhs_message: {nhs_message}, safety_check: {safetey_check}, user_message: {user_message}, added_context: {added_context}"
            response = self.get_ai_response(prompt)
            return response
            
        except Exception as e:
            print(f"Error in conversation agent: {e}")
            return "I'm having trouble processing that right now. Could you try rephrasing your message?"