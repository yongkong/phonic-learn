from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(20), nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    description = Column(String(200), nullable=True)
    target_grades = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    sub_scenes = relationship("SubScene", back_populates="scene", order_by="SubScene.sort_order")


class SubScene(Base):
    __tablename__ = "sub_scenes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"), nullable=False)
    name = Column(String(50), nullable=False)
    icon = Column(String(20), nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    description = Column(String(200), nullable=True)
    illustration_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    scene = relationship("Scene", back_populates="sub_scenes")
    scene_words = relationship("SceneWord", back_populates="sub_scene")
