from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.word import Word, SceneWord
from app.models.learning_record import LearningRecord
from app.schemas.word import WordListItem, WordDetailResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/words", tags=["words"])


@router.get(
    "/sub-scenes/{sub_scene_id}/words",
    response_model=list[WordListItem],
    summary="获取子场景下单词列表",
)
def get_sub_scene_words(
    sub_scene_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取子场景下的所有单词，含学习状态"""
    scene_words = (
        db.query(SceneWord)
        .filter(SceneWord.sub_scene_id == sub_scene_id)
        .order_by(SceneWord.sort_order)
        .all()
    )

    if not scene_words:
        return []

    # 获取学习记录
    word_ids = [sw.word_id for sw in scene_words]
    records = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == user.id,
            LearningRecord.word_id.in_(word_ids),
        )
        .all()
    )
    record_map = {r.word_id: r for r in records}

    result = []
    for sw in scene_words:
        word = db.query(Word).filter(Word.id == sw.word_id).first()
        if not word:
            continue

        record = record_map.get(sw.word_id)

        result.append(
            WordListItem(
                id=word.id,
                spelling=word.spelling,
                emoji=word.emoji,
                phonetic_us=word.phonetic_us,
                meanings=word.meanings,
                image_url=word.image_url,
                audio_filename=word.audio_filename,
                learning_status=record.status if record else "new",
                pronunciation_score=record.pronunciation_score if record else None,
            )
        )

    return result


@router.get(
    "/{word_id}", response_model=WordDetailResponse, summary="获取单词详情"
)
def get_word(
    word_id: int,
    db: Session = Depends(get_db),
):
    """获取单词完整信息（五维数据）"""
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="单词不存在")

    return WordDetailResponse(
        id=word.id,
        spelling=word.spelling,
        phonetic_us=word.phonetic_us,
        phonetic_uk=word.phonetic_uk,
        meanings=word.meanings,
        example_sentences=word.example_sentences,
        phonic_analysis=word.phonic_analysis,
        memory_tips=word.memory_tips,
        image_url=word.image_url,
        emoji=word.emoji,
        audio_filename=word.audio_filename,
        tags=word.tags or [],
        grade_range=word.grade_range,
    )
