from datetime import datetime

from pydantic import BaseModel


class SubSceneResponse(BaseModel):
    id: int
    name: str
    icon: str | None = None
    sort_order: int
    description: str | None = None
    illustration_url: str | None = None
    word_count: int = 0
    learned_count: int = 0
    is_unlocked: bool = True

    class Config:
        from_attributes = True


class SceneResponse(BaseModel):
    id: int
    name: str
    icon: str
    sort_order: int
    description: str | None = None
    target_grades: str
    sub_scenes: list[SubSceneResponse] = []
    progress: float = 0.0  # 0.0 - 1.0

    class Config:
        from_attributes = True
