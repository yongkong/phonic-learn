from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    JSON,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class LearningRecord(Base):
    """学习记录 - 每个用户对每个单词一条记录"""

    __tablename__ = "learning_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    status = Column(
        String(20), nullable=False, default="new"
    )  # new / learning / familiar / mastered
    dimension_progress = Column(
        JSON, nullable=False
    )  # {"form": {"completed": true}, "meaning": {...}, ...}
    pronunciation_score = Column(Integer, nullable=True)
    spelling_attempts = Column(Integer, default=0)
    spelling_correct = Column(Integer, default=0)
    last_learned_at = Column(DateTime, nullable=True)
    last_review_at = Column(DateTime, nullable=True)
    next_review_at = Column(DateTime, nullable=True)
    review_interval_days = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    repetition_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="learning_records")
    word = relationship("Word", back_populates="learning_records")

    __table_args__ = (
        CheckConstraint(
            "pronunciation_score >= 0 AND pronunciation_score <= 100",
            name="check_pronunciation_score",
        ),
    )


class LearningSession(Base):
    """学习会话 - 记录每次学习的整体情况"""

    __tablename__ = "learning_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sub_scene_id = Column(Integer, ForeignKey("sub_scenes.id"), nullable=True)
    session_type = Column(
        String(20), nullable=False
    )  # scene_learning / review / practice
    words_count = Column(Integer, default=0)
    avg_pronunciation_score = Column(Integer, nullable=True)
    total_spelling_attempts = Column(Integer, default=0)
    total_spelling_correct = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="learning_sessions")
