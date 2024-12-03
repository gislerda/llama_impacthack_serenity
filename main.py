from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TG_BOT_TOKEN
from bot.database.database import (
    init_db, 
    get_or_create_user, 
    log_interaction, 
    get_memories,
    store_memory
)
from bot.agents.conversation_agent import ConversationAgent
from bot.agents.vision_agent import VisionAgent
from bot.agents.nhs_agent import NHSAgent
from bot.agents.decider_agent import DeciderAgent
from bot.agents.safety_agent import SafetyAgent
from bot.agents.memory_agent import MemoryAgent
from bot.agents.sentiment_agent import SentimentAgent
from bot.agents.suggestion_agent import SuggestionAgent
from bot.agents.coping_agent import CopingAgent
from bot.agents.moderator_agent import ModeratorAgent
from bot.agents.checkin_agent import CheckinAgent

import asyncio
import json
from datetime import datetime

# Path to the JSON file
json_file_path = "./data/sentiments.json"
import os


# Function to load the JSON data from the file
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return {"sentiment_analysis": []}

# Function to save the JSON data back to the file
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Function to append a sentiment entry to the JSON file
def append_sentiment_entry(file_path, sentiment, loneliness_level, message, critical_signal):
    # Load existing data
    data = load_data(file_path)
    
    # Create a new entry
    new_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",  # Current UTC time in ISO 8601 format
        "sentiment": sentiment,
        "loneliness_level": loneliness_level,
        "message": message,
        "critical_signal": critical_signal
    }
    
    # Append the new entry
    data["sentiment_analysis"].append(new_entry)
    
    # Save updated data
    save_data(file_path, data)
    return data

# Example usage during runtime
#append_sentiment_entry(
#    json_file_path, 
#    sentiment="neutral", 
#    loneliness_level=2, 
#    message="I'm okay, just a regular day.", 
#    critical_signal=False
#)

#append_sentiment_entry(
#    json_file_path, 
#    sentiment="positive", 
#    loneliness_level=1, 
#    message="Had a wonderful chat with friends!", 
#    critical_signal=False
#)

# Load and print the current data
current_data = load_data(json_file_path)
print(json.dumps(current_data, indent=4))




class LonelinessBot:
    def __init__(self):
        self.conversation_agent = ConversationAgent()
        self.vision_agent = VisionAgent()
        self.decider_agent = DeciderAgent()
        self.nhs_agent = NHSAgent()
        self.safety_agent = SafetyAgent()
        self.memory_agent = MemoryAgent()
        self.sentiment_agent = SentimentAgent()
        self.suggestion_agent = SuggestionAgent()
        self.coping_agent = CopingAgent()
        self.moderator_agent = ModeratorAgent()
        self.checkin_agent = CheckinAgent()


    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Command handler for /start"""
        user = update.effective_user
        get_or_create_user(user.id, user.first_name)  # Create user record
        
        welcome_message = (
            f"👋 Hello {user.first_name}! I'm here to chat and keep you company.\n\n"
            "You can:\n"
            "- Send me messages to chat\n"
            "- Share images for me to look at\n"
            "- Use /memories to see what I remember about our conversations\n\n"
            "How are you feeling today?"
        )
        await update.message.reply_text(welcome_message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id  # Get Telegram user ID directly
        user_message = update.message.text
        user = get_or_create_user(user_id, update.effective_user.first_name)
        
        if not user:
            await update.message.reply_text("Sorry, I'm having trouble processing your message.")
            return
            
        added_context = "No additional context."
        #Safety
        safety_check = await self.safety_agent.check_message(user_message)
        #print(safety_check)
        #Memory
        #print(f"user.id: {user.id}\nuser_id: {user_id}user.telegram_id: {user.telegram_id}")
        await self.memory_agent.process_message(user_message,safety_check,user_id=user_id)
        safety_response = "Safety Response not relevant"
        print("Safety check done")
        if not safety_check["is_safe"]:
            safety_response = await self.nhs_agent.process_message(message = user_message, user_id=user_id)
        else:
            #Sentiment
            sentiment_response = await self.sentiment_agent.process_message(safety_check=safety_check,user_message= user_message, user_id = user_id)
            print(f"sentiment_response: {sentiment_response}")
            sentiment_data = append_sentiment_entry(json_file_path,sentiment=sentiment_response, loneliness_level=None, message = update.message.text, critical_signal=None)
            #Decider
            decider_response = await self.decider_agent.process_message(message=update.message.text,
            sentiment=sentiment_response, user_id= user_id) 
            #TODO: Update Loneliness level
            
            # Example usage during runtime
#append_sentiment_entry(
#    json_file_path, 
#    sentiment="neutral", 
#    loneliness_level=2, 
#    message="I'm okay, just a regular day.", 
#    critical_signal=False
#)
            
      
            #Event suggestion or Identity
            if decider_response == "suggestion_agent":
                print("ACTIVATE SUGGESTION AGENT")
                suggestion_response = await self.suggestion_agent.process_message(
                    user_message=user_message,
                    user_id=user_id
                )
                added_context = "SENTIMENT_HIST: " + str(sentiment_data)+ suggestion_response
                event_data = {
                    "context": added_context,
                    "user_message": user_message,
                    "user_id": user_id
                }

                async def scheduled_follow_up():
                    await asyncio.sleep(30)  # Wait for 12 seconds
                    print(f"Scheduled follow-up triggered: {json.dumps(event_data, indent=2)}")
                    # Add your follow-up logic here¨
                    #response = await self.checkin_agent.process_message(user_message=user_message,user_id=user_id, context="")
                    await update.message.reply_text("Did you end up joining the event? What was the most exciting thing there?")

                
                # Schedule the task without waiting for it
                asyncio.create_task(scheduled_follow_up())

            elif decider_response == "coping_agent":
                print("ACTIVATE SUGGESTION AGENT")
                suggestion_response = await self.coping_agent.process_message(
                    user_message=user_message,
                    user_id=user_id
                )
                added_context = "SENTIMENT_HIST: " + str(sentiment_data) + suggestion_response
            elif decider_response == "listen_agent":
                self.conversation_agent.system_prompt += "KEEP YOUR ANSWER TO ONE SHORT SENTENCE!\n One line maximum, e.g. ending on a short question showing GENUINE interest. Avoid empty words"
            else:  # identity case
                added_context = "SENTIMENT_HIST: " + str(sentiment_data) + user_message

            memory_data = await self.memory_agent.get_memory_context(user_id=user_id)
            print(f"MEMORY DATA: {memory_data}")
            added_context = "SENTIMENT_HIST: " + str(sentiment_data)  + "IMPORTANT MEMORIES " + str(memory_data)

        #TODO
        #
        #log_interaction(user_id, update.message.text)
        
        # Conversation Agent
        response = await self.conversation_agent.process_message(nhs_message=safety_response,safetey_check=safety_check,user_message=user_message,added_context=added_context,user_id=user.id)

        # Safety Output
        safety_check = await self.safety_agent.check_message(response)
        print("Safety check done")
        if not safety_check["is_safe"]:
            print(f"OUTPUT SAFETY: {safety_check}")
            safety_response = await self.moderator_agent.process_message(message = response, user_id=user.id)
            await update.message.reply_text(safety_response)
        else:
            
            await update.message.reply_text(response)

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        photo = update.message.photo[-1]
        caption = update.message.caption
        
        description = await self.vision_agent.process_image(
            photo=photo,
            user_id=update.effective_user.id,
            caption=caption
        )
        
        #await update.message.reply_text(response)

        user_id = update.effective_user.id  # Get Telegram user ID directly
        user_message = "No user message"
        if caption is not None:
            user_message = caption
            
        user = get_or_create_user(user_id, update.effective_user.first_name)
        
        if not user:
            await update.message.reply_text("Sorry, I'm having trouble processing your message.")
            return
            
        added_context = "No additional context."
        #Safety
        safety_check = await self.safety_agent.check_message(f"CAPTION:{caption} DESCRIPTION:{description}")
        #print(safety_check)
        #Memory
        #print(f"user.id: {user.id}\nuser_id: {user_id}user.telegram_id: {user.telegram_id}")
        await self.memory_agent.process_message(user_message,safety_check,user_id=user_id)
        safety_response = "Safety Response not relevant"
        print("Safety check done")
        if not safety_check["is_safe"]:
            safety_response = await self.nhs_agent.process_message(message = user_message, user_id=user.id)
        else:
            #Sentiment
            sentiment_response = await self.sentiment_agent.process_message(safety_check=safety_check,user_message= user_message, user_id = user.id)
            print(f"sentiment_response: {sentiment_response}")
            sentiment_data = append_sentiment_entry(json_file_path,sentiment=sentiment_response, loneliness_level=None, message = update.message.text, critical_signal=None)
            #Decider
            decider_response = await self.decider_agent.process_message(message=update.message.text,
            sentiment=sentiment_response, user_id= user_id
        ) 
    
        self.conversation_agent.system_prompt += "KEEP YOUR ANSWER Concise!\n One line maximum, e.g. ending on a short question showing GENUINE interest. Avoid empty words"
        added_context = "SENTIMENT_HIST: " + str(sentiment_data) + user_message

        #TODO
        #
        #log_interaction(user_id, update.message.text)
        added_context += "IMAGE DESCRIPTION: " + description
        # Conversation Agent
        print(added_context)
        print(f"Convo Agent {self.conversation_agent.system_prompt}")
        response = await self.conversation_agent.process_message(nhs_message=safety_response,safetey_check=safety_check,user_message=user_message,added_context=added_context,user_id=user.id)

        # Safety Output
        safety_check = await self.safety_agent.check_message(response)
        print("Safety check done")
        if not safety_check["is_safe"]:
            print(f"OUTPUT SAFETY: {safety_check}")
            safety_response = await self.moderator_agent.process_message(message = response, user_id=user.id)
            await update.message.reply_text(safety_response)
        else:
            
            await update.message.reply_text(response)



    async def check_memories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Command handler for /memories"""
        user_id = update.effective_user.id
        all_memories = get_memories(user_id)
        
        response = "🧠 Memory Status:\n\n"
        
        # Separate memories by type and importance
        text_memories = [m for m in all_memories if m.memory_type == 'text']
        image_memories = [m for m in all_memories if m.memory_type == 'image']
        
        # Important Text Memories
        important_text = [m for m in text_memories if m.is_important]
        if important_text:
            response += "⭐ Important Information:\n"
            for memory in important_text:
                response += f"📌 {memory.category.title()}: {memory.content}\n"
            response += "\n"
        
        # Regular Text Memories
        regular_text = [m for m in text_memories if not m.is_important]
        if regular_text:
            response += "💭 Other Information:\n"
            for memory in regular_text:
                response += f"📝 {memory.category.title()}: {memory.content}\n"
            response += "\n"
        
        # Important Image Memories
        important_images = [m for m in image_memories if m.is_important]
        if important_images:
            response += "🖼️ Important Images:\n"
            for memory in important_images:
                response += f"📌 {memory.content[:100]}...\n"
            response += "\n"
        
        # Recent Image Memories
        recent_images = [m for m in image_memories if not m.is_important][:5]
        if recent_images:
            response += "📸 Recent Images:\n"
            for memory in recent_images:
                response += f"💭 {memory.content}...\n"
        
        if not all_memories:
            response += "No memories stored yet! Share some information or images with me."
        
        await update.message.reply_text(response)

def main():
    # Initialize database
    init_db()
    print("Database initialized")
    
    # Initialize bot
    bot = LonelinessBot()
    application = Application.builder().token(TG_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, bot.handle_photo))
    application.add_handler(CommandHandler("memories", bot.check_memories))

    # Start the bot
    print("Starting bot...")
    application.run_polling()

if __name__ == '__main__':
    main()