from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    spelling = Column(String(50), nullable=False, unique=True)
    phonetic_us = Column(String(100), nullable=True)
    phonetic_uk = Column(String(100), nullable=True)
    meanings = Column(JSON, nullable=False)  # [{"pos": "n.", "cn": "橙子"}]
    example_sentences = Column(
        JSON, nullable=False
    )  # [{"en": "...", "cn": "...", "audio": "..."}]
    phonic_analysis = Column(
        JSON, nullable=False
    )  # {"syllables": [...], "letter_sounds": [...]}
    memory_tips = Column(
        JSON, nullable=True
    )  # [{"type": "image", "content": "..."}]
    image_url = Column(String(255), nullable=True)
    emoji = Column(String(10), nullable=True)
    audio_filename = Column(String(100), nullable=True)
    grade_range = Column(String(10), nullable=False)
    tags = Column(JSON, nullable=True)  # ["水果", "颜色"]
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    scene_words = relationship("SceneWord", back_populates="word")
    learning_records = relationship("LearningRecord", back_populates="word")


class SceneWord(Base):
    __tablename__ = "scene_words"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sub_scene_id = Column(Integer, ForeignKey("sub_scenes.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    # Relationships
    sub_scene = relationship("SubScene", back_populates="scene_words")
    word = relationship("Word", back_populates="scene_words")
