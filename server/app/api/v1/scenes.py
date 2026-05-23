from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.scene import Scene, SubScene
from app.models.word import SceneWord
from app.models.learning_record import LearningRecord
from app.schemas.scene import SceneResponse, SubSceneResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/scenes", tags=["scenes"])


@router.get("", response_model=list[SceneResponse], summary="获取场景列表")
def get_scenes(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取所有场景列表，含子场景和进度"""
    scenes = db.query(Scene).order_by(Scene.sort_order).all()

    result = []
    for scene in scenes:
        sub_scenes_data = []
        total_words = 0
        total_learned = 0

        for sub_scene in scene.sub_scenes:
            # 计算单词数
            scene_words = (
                db.query(SceneWord)
                .filter(SceneWord.sub_scene_id == sub_scene.id)
                .all()
            )
            word_count = len(scene_words)
            total_words += word_count

            # 计算已学数
            word_ids = [sw.word_id for sw in scene_words]
            if word_ids:
                learned_count = (
                    db.query(LearningRecord)
                    .filter(
                        LearningRecord.user_id == user.id,
                        LearningRecord.word_id.in_(word_ids),
                        LearningRecord.status != "new",
                    )
                    .count()
                )
            else:
                learned_count = 0

            total_learned += learned_count

            sub_scenes_data.append(
                SubSceneResponse(
                    id=sub_scene.id,
                    name=sub_scene.name,
                    icon=sub_scene.icon,
                    sort_order=sub_scene.sort_order,
                    description=sub_scene.description,
                    illustration_url=sub_scene.illustration_url,
                    word_count=word_count,
                    learned_count=learned_count,
                    is_unlocked=True,  # MVP 全部解锁
                )
            )

        progress = total_learned / total_words if total_words > 0 else 0.0

        result.append(
            SceneResponse(
                id=scene.id,
                name=scene.name,
                icon=scene.icon,
                sort_order=scene.sort_order,
                description=scene.description,
                target_grades=scene.target_grades,
                sub_scenes=sub_scenes_data,
                progress=round(progress, 2),
            )
        )

    return result


@router.get("/{scene_id}", response_model=SceneResponse, summary="获取场景详情")
def get_scene(
    scene_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取单个场景详情"""
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(status_code=404, detail="场景不存在")

    # 复用上面的逻辑
    sub_scenes_data = []
    total_words = 0
    total_learned = 0

    for sub_scene in scene.sub_scenes:
        scene_words = (
            db.query(SceneWord).filter(SceneWord.sub_scene_id == sub_scene.id).all()
        )
        word_count = len(scene_words)
        total_words += word_count

        word_ids = [sw.word_id for sw in scene_words]
        if word_ids:
            learned_count = (
                db.query(LearningRecord)
                .filter(
                    LearningRecord.user_id == user.id,
                    LearningRecord.word_id.in_(word_ids),
                    LearningRecord.status != "new",
                )
                .count()
            )
        else:
            learned_count = 0

        total_learned += learned_count

        sub_scenes_data.append(
            SubSceneResponse(
                id=sub_scene.id,
                name=sub_scene.name,
                icon=sub_scene.icon,
                sort_order=sub_scene.sort_order,
                description=sub_scene.description,
                illustration_url=sub_scene.illustration_url,
                word_count=word_count,
                learned_count=learned_count,
                is_unlocked=True,
            )
        )

    progress = total_learned / total_words if total_words > 0 else 0.0

    return SceneResponse(
        id=scene.id,
        name=scene.name,
        icon=scene.icon,
        sort_order=scene.sort_order,
        description=scene.description,
        target_grades=scene.target_grades,
        sub_scenes=sub_scenes_data,
        progress=round(progress, 2),
    )
