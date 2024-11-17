from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from .models import Base, User, Interaction, ScheduledEvent, Memory
from config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized successfully")

def get_or_create_user(telegram_id: int, name: str = None) -> User:
    """Get existing user or create new one"""
    db = next(get_db())
    try:
        print(f"TELEGRAM ID: {telegram_id}")
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id, name=name)
            user.id = telegram_id
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created new user: {telegram_id}")

        return user
    except Exception as e:
        print(f"Error in get_or_create_user: {e}")
        db.rollback()
        return None

def store_memory(user_id: int, content: str, memory_type: str, category: str, 
                is_important: bool = False, confidence: float = 1.0, context: str = None):
    """Store a memory, creating user if needed"""
    db = next(get_db())
    try:
        # Get user with the same session
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            user = get_or_create_user(user_id)
            if not user:
                return None
            
        memory = Memory(
            user_id=user_id,
            content=content,
            memory_type=memory_type,
            category=category,
            is_important=is_important,
            confidence=confidence,
            context=context
        )
        db.add(memory)
        db.commit()
        db.refresh(memory)
        print(f"Stored {memory_type} memory for user {user_id}: {content}...")
        return memory
    except Exception as e:
        print(f"Error storing memory: {e}")
        db.rollback()
        return None

def get_memories(telegram_id: int, memory_type: str = None):
    """Get memories for user, creating user if needed"""
    try:
        db = next(get_db())
        user = get_or_create_user(telegram_id)
        print(f"user: {user} Type {type(user)} userid: {user.id}")
        if not user:
            return []
            
        query = db.query(Memory).filter(Memory.user_id == user.id)
        if memory_type:
            query = query.filter(Memory.memory_type == memory_type)
        return query.order_by(Memory.created_at.desc()).all()
    except Exception as e:
        print(f"Error retrieving memories: {e}")
        return []

def get_important_memories(telegram_id: int):
    """Get important memories for user, creating user if needed"""
    try:
        db = next(get_db())
        user = get_or_create_user(telegram_id)
        if not user:
            return []
            
        return db.query(Memory)\
            .filter(Memory.user_id == user.id, Memory.is_important == True)\
            .order_by(Memory.created_at.desc())\
            .all()
    except Exception as e:
        print(f"Error retrieving important memories: {e}")
        return []

def log_interaction(user_id: int, message: str, emotional_state: str = None):
    """Log an interaction, creating user if needed"""
    try:
        db = next(get_db())
        user = get_or_create_user(user_id)
        if not user:
            return None
            
        interaction = Interaction(
            user_id=user.id,
            message=message,
            emotional_state=emotional_state
        )
        db.add(interaction)
        db.commit()
        return interaction
    except Exception as e:
        print(f"Error logging interaction: {e}")
        db.rollback()
        return None