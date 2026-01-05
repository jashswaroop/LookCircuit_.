from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base  # Need to define Base in session or base class

# Using declarative base is standard
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Profile fields
    gender = Column(String, nullable=True)
    age_range = Column(String, nullable=True)
    skin_tone = Column(String, nullable=True)
    face_shape = Column(String, nullable=True)
    body_type = Column(String, nullable=True)
