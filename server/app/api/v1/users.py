import secrets
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.learning_record import LearningRecord, LearningSession
from app.schemas.user import RegisterRequest, UserResponse, UserStatsResponse, WeeklyStat
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, summary="用户注册")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册，昵称+年级，返回 token"""
    # 检查昵称是否重复
    existing = db.query(User).filter(User.nickname == request.nickname).first()
    if existing:
        raise HTTPException(status_code=409, detail="该昵称已被使用")

    # 生成 token
    token = secrets.token_hex(32)

    user = User(
        nickname=request.nickname,
        grade=request.grade,
        token=token,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
def get_me(user: User = Depends(get_current_user)):
    return user


@router.get("/me/stats", response_model=UserStatsResponse, summary="获取学习统计")
def get_me_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = datetime.utcnow().date()

    # 获取所有学习记录
    records = db.query(LearningRecord).filter(LearningRecord.user_id == user.id).all()

    total_learned = len([r for r in records if r.status != "new"])
    total_mastered = len([r for r in records if r.status == "mastered"])
    pending_review = len(
        [
            r
            for r in records
            if r.next_review_at and r.next_review_at <= datetime.utcnow()
        ]
    )

    # 今日学习数
    today_records = [
        r for r in records if r.last_learned_at and r.last_learned_at.date() == today
    ]
    today_learned = len(today_records)

    # 平均发音分数
    scores = [r.pronunciation_score for r in records if r.pronunciation_score]
    avg_score = int(sum(scores) / len(scores)) if scores else None

    # 连续学习天数 (简化计算)
    study_streak = 1  # MVP 简化

    # 本周统计 (简化)
    weekly_stats = []
    for i in range(6, -1, -1):
        day = today - __import__("datetime").timedelta(days=i)
        day_records = [
            r
            for r in records
            if r.last_learned_at and r.last_learned_at.date() == day
        ]
        weekly_stats.append(
            WeeklyStat(date=day.isoformat(), words_count=len(day_records))
        )

    return UserStatsResponse(
        total_learned=total_learned,
        total_mastered=total_mastered,
        total_pending_review=pending_review,
        study_streak_days=study_streak,
        today_learned=today_learned,
        today_target=20,
        weekly_stats=weekly_stats,
        average_pronunciation_score=avg_score,
    )
