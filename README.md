# Llama Impact Hack: London

This repository contains a Telegram bot designed to help alleviate loneliness through AI-powered conversations and image interactions. Built during the Llama Impact Hackathon: London hosted by Cerebral Valley x Meta.

<p align="center">
  <img src="/llama-impact-london.jpeg" width="400"/>
</p>

## Features

### Core Functionality
- 💬 **Natural Conversations**: Empathetic AI responses focused on emotional well-being
- 🖼️ **Image Processing**: Analysis and memory storage of shared images
- 🧠 **Memory System**: 
  - Confidence-based memory storage
  - Important memory categorization (life events, background, preferences, etc.)
  - Contextual recall for both text and images
- 📅 **Event Scheduling**: Future reminders and check-ins

### Commands
- `/start` - Begin conversation with the bot
- `/memories` - View stored memories organized by importance and type
- Send text messages for general conversation
- Share images for visual analysis and memory storage

## Setup Instructions

### Prerequisites
- Python 3.10.15
- Telegram Bot Token
- Groq API Key

### Environment Setup
1. Clone the repository:
```bash
git clone https://github.com/kyomangold/llama-impact-hack.git
cd llama-impact-hack
```

2. Create and activate virtual environment:
```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
TG_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=sqlite:///bot_database.db
```

### Running the Bot
From the llama-impact-hack directory:
```bash
python -m bot.main
```

## Technical Stack

### Models
- **Text Generation**: Llama 3.2 via Groq API
- **Vision Tasks**: Llama 3.2 Vision Preview via Groq API

### Components
- **Frontend**: Telegram Bot API
- **Backend**: Python async architecture
- **Database**: SQLite with SQLAlchemy
- **AI Integration**: Groq API

## Development

### Project Structure
```
llama-impact-hack/
├── .env
├── requirements.txt
├── config.py
├── bot/
│   ├── __init__.py
│   ├── main.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── database.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── conversation_agent.py
│   │   ├── suggestion_agent.py
│   │   ├── checkin_agent.py
│   │   └── vision_agent.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
```

### Database Models
- `User`: User profiles and preferences
- `Interaction`: Chat history and emotional states
- `Memory`: Unified storage for text and image memories with importance tracking
- `ScheduledEvent`: Future events and reminders

### Memory System
The bot uses a sophisticated memory system that:
- Analyzes conversations for important information
- Stores memories with confidence scores
- Categorizes memories (life events, background, preferences, emotional patterns, challenges)
- Maintains context for both text conversations and images
- Displays memories organized by type and importance using `/memories`

Memory Categories:
1. Major Life Events (relationships, career changes, etc.)
2. Personal Background (family, career, education)
3. Significant Preferences (values, goals, aspirations)
4. Emotional Patterns (challenges, mental health, support systems)
5. Current Challenges (ongoing struggles, decisions, transitions)

## Links
- 🤗 [Models on Hugging Face](https://huggingface.co/meta-llama)
- 📝 [Meta AI Blog](https://ai.meta.com/blog/)
- 🌐 [Llama Website](https://llama.meta.com/)
- 🚀 [Get Started with Llama](https://llama.meta.com/get-started/)

## Contributing
Feel free to submit issues and enhancement requests!

## License
This project is licensed under the terms of the MIT license.
