from .base_agent import BaseAgent
from typing import Dict

class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = """
        Analyze the user's message to determine sentiment, loneliness level, and critical signal in maximum of 10 words.
        """


        """
        "type": "function",
        "function": {
            "name": "analyze_sentiment",
            "description": "Analyze the user's message to determine sentiment, loneliness level, and critical signal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The text message to analyze"
                    },
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "neutral", "negative"],
                        "description": "The sentiment of the message"
                    },
                    "loneliness_level": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "A scale from 1 (not lonely) to 5 (very lonely)"
                    },
                    "critical_signal": {
                        "type": "boolean",
                        "description": "Whether the message indicates an urgent need for support"
                    }
                },
                "required": ["sentiment", "loneliness_level", "critical_signal"]
        #""
        self.tools = [
    {
        "type": "function",
        "function": {
            "name": "analyze_sentiment",
            "description": "Analyze the user's message to determine sentiment, loneliness level, and critical signal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The text message to analyze"
                    },
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "neutral", "negative"],
                        "description": "The sentiment of the message"
                    },
                    "loneliness_level": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "A scale from 1 (not lonely) to 5 (very lonely)"
                    },
                    "critical_signal": {
                        "type": "boolean",
                        "description": "Whether the message indicates an urgent need for support"
                    }
                },
                "required": ["sentiment", "loneliness_level", "critical_signal"]
            }
        }
    }
]"""
        self.tool_choice = "auto"

    async def process_message(self, safety_check: Dict, user_message: str,  user_id: int) -> str:
        try:
            #TODO: Store / Update Sentiment somewhere in ze cloud
            message = f"safety_check: {safety_check}, user_message: {user_message}"
            response = self.get_ai_response(message)
            return response

        except Exception as e:
            print(f"Error in conversation agent: {e}")
            return "I'm having trouble processing that right now. Could you try rephrasing your message?"
