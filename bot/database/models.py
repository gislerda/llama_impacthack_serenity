from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String)
    age = Column(Integer, nullable=True)
    occupation = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Interaction(Base):
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text)
    emotional_state = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ScheduledEvent(Base):
    __tablename__ = 'scheduled_events'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_type = Column(String)
    scheduled_time = Column(DateTime)
    details = Column(Text)
    completed = Column(Integer, default=0)

class Memory(Base):
    __tablename__ = 'memories'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)  # The information or image description
    memory_type = Column(String)  # 'text' or 'image'
    category = Column(String)  # e.g., 'background', 'milestone', 'image'
    is_important = Column(Boolean, default=False)
    confidence = Column(Float)
    context = Column(Text, nullable=True)  # Additional context (e.g., original message, image URL)
    created_at = Column(DateTime, default=datetime.utcnow)