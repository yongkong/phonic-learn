from datetime import datetime

from pydantic import BaseModel, Field


class StartSessionRequest(BaseModel):
    sub_scene_id: int
    session_type: str = "scene_learning"  # scene_learning / review / practice


class CompleteDimensionRequest(BaseModel):
    word_id: int
    dimension: str = Field(
        ..., pattern="^(form|meaning|sound|memory|usage)$",
        description="五维之一: form/meaning/sound/memory/usage"
    )
    score: int | None = Field(None, ge=0, le=100, description="维度评分")


class CompleteWordRequest(BaseModel):
    word_id: int
    session_id: int
    final_pronunciation_score: int | None = Field(None, ge=0, le=100)
    spelling_correct: bool = True


class RecordPronunciationRequest(BaseModel):
    word_id: int
    score: int = Field(..., ge=0, le=100, description="跟读评分")


class RecordSpellingRequest(BaseModel):
    word_id: int
    correct: bool


class LearningStatsResponse(BaseModel):
    total_words: int = 0
    learned_words: int = 0
    mastered_words: int = 0
    pending_review: int = 0
    today_learned: int = 0
    today_target: int = 20
    average_score: float | None = None
