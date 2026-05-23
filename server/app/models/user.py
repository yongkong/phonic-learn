from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String(50), nullable=False, unique=True)
    grade = Column(Integer, nullable=False)
    avatar_url = Column(String(255), nullable=True)
    token = Column(String(64), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    learning_records = relationship("LearningRecord", back_populates="user")
    learning_sessions = relationship("LearningSession", back_populates="user")

    __table_args__ = (
        CheckConstraint("grade >= 1 AND grade <= 6", name="check_grade_range"),
    )
