from .base_agent import BaseAgent
from typing import List, Dict
from ..database.database import store_memory, get_memories, get_important_memories

class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.memory_prompt = """
        Analyze the user's message for important information that should be remembered for future conversations.
        
        Consider information IMPORTANT if it falls into these categories:
        1. Major Life Events:
           - Relationships (engagements, marriages, breakups)
           - Career changes or achievements
           - Educational milestones
           - Moving homes/cities
           - Health situations
        
        2. Personal Background:
           - Family structure and relationships
           - Career/occupation
           - Education history
           - Living situation
           - Cultural background
        
        3. Significant Preferences:
           - Strong likes/dislikes
           - Important values or beliefs
           - Life goals or aspirations
           - Deal-breakers or boundaries
        
        4. Emotional Patterns:
           - Recurring emotional challenges
           - Mental health concerns
           - Support systems or lack thereof
           - Coping mechanisms
        
        5. Current Challenges:
           - Ongoing struggles
           - Major decisions
           - Life transitions
           - Personal development goals
        If you find important information, format it as:
        MEMORY: [the specific fact/information]
        CATEGORY: [life_event/background/preference/emotional/challenge]
        IMPORTANCE: true
        CONFIDENCE: [0.0-1.0]
        REASON: [why this is worth remembering for future conversations]
        Regular, non-important information (like casual preferences, daily activities, or general chat) should not be stored.
        If no important information is found, respond with "NO_MEMORY_NEEDED"""

    
    async def process_message(self, message: str, safety_check: Dict, user_id: int) -> None: 
            """Process and store memories from a message""" 
            try: 
                # Skip if message isn't safe 
                if not safety_check.get('is_safe', False): 
                    print("Skipping memory processing for unsafe message") 
                    return 
                    
                # Get existing memories for context 
                print(f"USERID IN MEMORY AGENT: {user_id}")
                important_memories = get_important_memories(user_id) 
                
                # Create context from memories 
                memory_context = "Important past information:\n" 
                for memory in important_memories: 
                    memory_context += f"- {memory.content}\n" 
                
                # Analyze for new memories 
                memory_analysis = self.get_ai_response( 
                    f"Previous context:\n{memory_context}\n\n" 
                    f"User message: {message}\n\n{self.memory_prompt}" 
                ) 
                
                # Store new memories if found 
                if "MEMORY:" in memory_analysis: 
                    memory_blocks = memory_analysis.split('MEMORY:')[1:] 
                    for block in memory_blocks: 
                        # Skip if this is just the NO_MEMORY_NEEDED message 
                        if "NO_MEMORY_NEEDED" in block: 
                            continue 
                            
                        memory_data = {} 
                        lines = block.strip().split('\n') 
                        memory_data['MEMORY'] = lines[0].strip() 
                        
                        for line in lines[1:]: 
                            if ':' in line: 
                                key, value = line.split(':', 1) 
                                memory_data[key.strip()] = value.strip() 
                        
                        # Only store if confidence exceeds threshold 
                        if 'MEMORY' in memory_data and 'CATEGORY' in memory_data: 
                            confidence = float(memory_data.get('CONFIDENCE', '0.0')) 
                            if confidence >= 0.7:  # Threshold for important memories 
                                store_memory( 
                                    user_id=user_id, 
                                    content=memory_data['MEMORY'], 
                                    memory_type='text', 
                                    category=memory_data.get('CATEGORY', 'general'), 
                                    is_important=True, 
                                    confidence=confidence, 
                                    context=message 
                                ) 
                                
            except Exception as e: 
                print(f"Error in memory agent: {e}") 
    
    async def get_memory_context(self, user_id: int) -> str: 
            """Get formatted context string from important memories""" 
            try: 
                important_memories = get_important_memories(user_id) 
                memory_context = "Important past information:\n" 
                for memory in important_memories: 
                    memory_context += f"- {memory.content}\n" 
                return memory_context 
            except Exception as e: 
                print(f"Error getting memory context: {e}") 
                return ""


        