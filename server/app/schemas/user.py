from datetime import datetime

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50, description="用户昵称")
    grade: int = Field(..., ge=1, le=6, description="年级 (1-6)")


class UserResponse(BaseModel):
    id: int
    nickname: str
    grade: int
    avatar_url: str | None = None
    token: str
    created_at: datetime

    class Config:
        from_attributes = True


class WeeklyStat(BaseModel):
    date: str
    words_count: int


class UserStatsResponse(BaseModel):
    total_learned: int = 0
    total_mastered: int = 0
    total_pending_review: int = 0
    study_streak_days: int = 0
    today_learned: int = 0
    today_target: int = 20
    weekly_stats: list[WeeklyStat] = []
    average_pronunciation_score: int | None = None
