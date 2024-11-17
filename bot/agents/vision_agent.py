import base64
from io import BytesIO
from telegram import PhotoSize
from .base_agent import BaseAgent
from ..database.database import store_memory, get_memories, get_important_memories

class VisionAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.vision_prompt = """
        You are analyzing an image shared by a user. Provide a thoughtful and engaging response that:
        - Describes what you see in detail
        - Makes personal connections when appropriate
        - Encourages further conversation about the image
        
        Additionally, determine if this image contains important emotional or memorable content that should be remembered long-term.
        If it does, start your response with [IMPORTANT MEMORY] and explain why.
        
        If the user has included a message with the image, please respond specifically to their comments about the image.
        """
        self.memory_prompt = """
        Based on the image analysis, determine if this is an important memory that should be stored long-term.
        Consider factors like:
        - Emotional significance
        - Personal milestones
        - Family moments
        - Special events
        
        Return your response in this format:
        Important: [true/false]
        Reason: [brief explanation]
        """

    async def process_image(self, photo: PhotoSize, user_id: int, caption: str = None) -> str:
        try:
            file = await photo.get_file()
            file_url = file.file_path
            
            # Get initial image analysis
            response = self.get_ai_response_with_image(
                caption if caption else "What do you see in this image?",
                file_url
            )
            
            # Store as memory if important
            is_important = "[IMPORTANT MEMORY]" in response
            store_memory(
                user_id=user_id,
                content=response,
                memory_type='image',
                category='image',
                is_important=is_important,
                confidence=0.9,
                context=file_url
            )
            
            return response
            
        except Exception as e:
            print(f"Error in vision agent: {e}")
            return "I'm having trouble processing that image right now. Could you tell me about it instead?"

    async def process_message(self, message: str, user_id: int) -> str:
        try:
            # Get recent memories for context
            recent_memories = get_memories(user_id, 'image')
            important_memories = get_important_memories(user_id)
            
            context_prompt = f"""
            User message: {message}
            
            Recent image context:
            {[memory.content for memory in recent_memories]}
            
            Important memories:
            {[memory.content for memory in important_memories]}
            
            Based on these memories and the user's message, provide a contextual response.
            If they're referencing a specific image or memory, acknowledge it specifically.
            """
            
            response = self.get_ai_response(context_prompt)
            return response
            
        except Exception as e:
            print(f"Error processing message with image context: {e}")
            return "I'm having trouble understanding the context. Could you please clarify?"

    def get_ai_response_with_image(self, text: str, image_url: str) -> str:
        try:
            messages = [
                #{"role": "system", "content": self.vision_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        },
                        {
                            "type": "text",
                            "text": f"SYSTEM PROMPT: {self.vision_prompt} \n\n USER ADDED CAPTION: {text}"
                        }
                    ]
                }
            ]
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error getting AI vision response: {e}")
            return "I'm having trouble analyzing this image right now. Could you tell me more about what you see?"