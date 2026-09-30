from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.learning_record import LearningRecord, LearningSession
from app.schemas.learning import (
    StartSessionRequest,
    CompleteDimensionRequest,
    CompleteWordRequest,
    RecordPronunciationRequest,
    RecordSpellingRequest,
    EndSessionRequest,
    LearningStatsResponse,
)
from app.api.deps import get_current_user

router = APIRouter(prefix="/learning", tags=["learning"])


@router.post("/start-session", summary="开始学习会话")
def start_session(
    request: StartSessionRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """开始新的学习会话"""
    session = LearningSession(
        user_id=user.id,
        sub_scene_id=request.sub_scene_id,
        session_type=request.session_type,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {"session_id": session.id, "message": "Session started"}


@router.post("/complete-dimension", summary="完成一个维度的学习")
def complete_dimension(
    request: CompleteDimensionRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """完成五维学习中的一个维度"""
    # 获取或创建学习记录
    record = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == user.id,
            LearningRecord.word_id == request.word_id,
        )
        .first()
    )

    if not record:
        record = LearningRecord(
            user_id=user.id,
            word_id=request.word_id,
            status="learning",
            dimension_progress={
                "form": {"completed": False},
                "meaning": {"completed": False},
                "sound": {"completed": False},
                "memory": {"completed": False},
                "usage": {"completed": False},
            },
        )
        db.add(record)

    # 更新维度进度
    now = datetime.utcnow().isoformat()
    record.dimension_progress[request.dimension] = {
        "completed": True,
        "score": request.score,
        "completed_at": now,
    }

    # 更新发音分数
    if request.dimension == "sound" and request.score:
        record.pronunciation_score = request.score

    # 更新学习时间
    record.last_learned_at = datetime.utcnow()

    # 检查是否所有维度都完成
    all_completed = all(
        v.get("completed", False) for v in record.dimension_progress.values()
    )

    db.commit()

    return {
        "word_id": request.word_id,
        "dimension": request.dimension,
        "completed": True,
        "all_dimensions_completed": all_completed,
    }


@router.post("/complete-word", summary="完成一个单词的全部学习")
def complete_word(
    request: CompleteWordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """完成一个单词的五维学习"""
    record = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == user.id,
            LearningRecord.word_id == request.word_id,
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="学习记录不存在")

    # 更新状态
    record.status = "familiar"
    if request.final_pronunciation_score:
        record.pronunciation_score = request.final_pronunciation_score

    # 更新拼写记录
    if request.spelling_correct:
        record.spelling_correct += 1
    record.spelling_attempts += 1

    # 计算下次复习时间 (简化版 SM-2)
    if record.repetition_count == 0:
        interval = timedelta(minutes=20)  # 第一次复习：20分钟后
    elif record.repetition_count == 1:
        interval = timedelta(days=1)
    else:
        interval = timedelta(days=int(record.review_interval_days * record.ease_factor))

    record.next_review_at = datetime.utcnow() + interval
    record.last_review_at = datetime.utcnow()
    record.repetition_count += 1

    # 更新会话
    session = (
        db.query(LearningSession)
        .filter(LearningSession.id == request.session_id)
        .first()
    )
    if session:
        session.words_count += 1
        if request.final_pronunciation_score:
            if session.avg_pronunciation_score:
                session.avg_pronunciation_score = (
                    session.avg_pronunciation_score + request.final_pronunciation_score
                ) // 2
            else:
                session.avg_pronunciation_score = request.final_pronunciation_score

    db.commit()

    return {
        "word_id": request.word_id,
        "status": record.status,
        "next_review_at": record.next_review_at.isoformat(),
    }


@router.post("/record-pronunciation", summary="提交跟读评分")
def record_pronunciation(
    request: RecordPronunciationRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """提交跟读评分"""
    record = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == user.id,
            LearningRecord.word_id == request.word_id,
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="学习记录不存在")

    record.pronunciation_score = request.score
    db.commit()

    return {"word_id": request.word_id, "score": request.score}


@router.post("/record-spelling", summary="提交拼写练习结果")
def record_spelling(
    request: RecordSpellingRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """提交拼写练习结果"""
    record = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == user.id,
            LearningRecord.word_id == request.word_id,
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="学习记录不存在")

    record.spelling_attempts += 1
    if request.correct:
        record.spelling_correct += 1

    db.commit()

    return {
        "word_id": request.word_id,
        "attempts": record.spelling_attempts,
        "correct": record.spelling_correct,
    }


@router.post("/end-session", summary="结束学习会话")
def end_session(
    request: EndSessionRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """结束学习会话（参数以请求体接收，与前端契约一致）"""
    session = (
        db.query(LearningSession)
        .filter(
            LearningSession.id == request.session_id,
            LearningSession.user_id == user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    session.duration_seconds = request.duration_seconds
    session.completed_at = datetime.utcnow()
    db.commit()

    return {"message": "Session ended", "session_id": request.session_id}


@router.get("/stats", response_model=LearningStatsResponse, summary="获取学习统计")
def get_learning_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户的学习统计"""
    records = db.query(LearningRecord).filter(LearningRecord.user_id == user.id).all()

    total = len(records)
    learned = len([r for r in records if r.status != "new"])
    mastered = len([r for r in records if r.status == "mastered"])
    pending = len(
        [
            r
            for r in records
            if r.next_review_at and r.next_review_at <= datetime.utcnow()
        ]
    )

    today = datetime.utcnow().date()
    today_count = len(
        [
            r
            for r in records
            if r.last_learned_at and r.last_learned_at.date() == today
        ]
    )

    scores = [r.pronunciation_score for r in records if r.pronunciation_score]
    avg = sum(scores) / len(scores) if scores else None

    return LearningStatsResponse(
        total_words=total,
        learned_words=learned,
        mastered_words=mastered,
        pending_review=pending,
        today_learned=today_count,
        average_score=avg,
    )
