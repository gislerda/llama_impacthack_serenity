from .base_agent import BaseAgent
from typing import List, Dict

class NHSAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "provide_health_guidance",
                    "description": "Provide NHS-based health guidance and emergency information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "response": {
                                "type": "string",
                                "description": "The health guidance response"
                            },
                            "urgency_level": {
                                "type": "string",
                                "enum": ["non_urgent", "111", "emergency"],
                                "description": "The level of medical attention needed"
                            },
                            "contact_info": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "Relevant NHS contact information"
                            }
                        },
                        "required": ["response", "urgency_level", "contact_info"]
                    }
                }
            }
        ]

    async def process_message(self, message: str, user_id: int) -> Dict:
        

        return "For emergencies: Call 999"