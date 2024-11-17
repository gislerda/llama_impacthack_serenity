from .base_agent import BaseAgent
from typing import List, Dict
import json

class DeciderAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "route_message",
                    "description": "Route the user's message to the appropriate agent(s)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "selected_agents": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": ["coping_agent","suggestion_agent", "listen_agent"]
                                },
                                "description": "The agents that should handle this message"
                            },
                            "explanation": {
                                "type": "string",
                                "description": "Explanation of why these agents were selected"
                            }
                        },
                        "required": ["selected_agents", "explanation"]
                    }
                }
            }
        ]

    async def process_message(self, message: str, sentiment: str,  user_id: int) -> Dict:
        try:
            self.system_prompt = """You are a routing agent that determines which specialized agent(s) should handle user messages.

            Available agents:
            - listen_agent: Answer only with a brief response. Use this if you feel the user message is "venting" or requires further context.
            - suggestion_agent: Suggests an activity to do
            - coping_agent: Suggests an appropriate coping strategy for the given situation

            Select the most appropriate agent(s) for each message."""
            
            self.tool_choice="required"
             

            prompt = f"usermessage: {message}, sentiment: {sentiment}"
            response = self.get_ai_response(prompt = prompt )

            if not response.tool_calls or not response.tool_calls[0].function.arguments:
                raise ValueError("No function call in response")
                
            # Parse the JSON string into a Python dictionary
            function_args = json.loads(response.tool_calls[0].function.arguments)
            
            print(f"Decider Agent Response: TYPE{type(function_args)}\n{function_args}")  # Now you can access it as a dictionary
            
            return function_args["selected_agents"][0]
            # Now you can access selected_agents directly
            return {
                "agents": function_args.get("selected_agents", ["conversation_agent"]),
                "reasoning": function_args.get("explanation", "Default routing to memory agent")
            }
            
        except Exception as e:
            print(f"Error in decider agent: {e}")
            return "conversation_agent"