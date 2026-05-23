"""场景种子数据"""

from app.models.scene import Scene, SubScene


def seed_scenes(db):
    """创建 3 scenes及其子场景"""

    # 检查是否已有数据
    if db.query(Scene).first():
        print("Scenes already exist, skipping")
        return

    scenes_data = [
        {
            "name": "我的家",
            "icon": "🏠",
            "sort_order": 1,
            "description": "认识家里的各个房间和日常用品",
            "target_grades": "1-2",
            "sub_scenes": [
                {"name": "厨房", "icon": "🍳", "sort_order": 1, "description": "厨房里的物品和食物"},
                {"name": "客厅", "icon": "🛋️", "sort_order": 2, "description": "客厅里的家具和物品"},
            ],
        },
        {
            "name": "我的学校",
            "icon": "🏫",
            "sort_order": 2,
            "description": "学校里的人和物品",
            "target_grades": "1-3",
            "sub_scenes": [
                {"name": "教室", "icon": "📚", "sort_order": 1, "description": "教室里的学习用品"},
            ],
        },
        {
            "name": "超市购物",
            "icon": "🛒",
            "sort_order": 3,
            "description": "在超市认识各种食物",
            "target_grades": "2-3",
            "sub_scenes": [
                {"name": "水果区", "icon": "🍎", "sort_order": 1, "description": "各种水果"},
            ],
        },
    ]

    for scene_data in scenes_data:
        sub_scenes_data = scene_data.pop("sub_scenes")

        scene = Scene(**scene_data)
        db.add(scene)
        db.flush()

        for sub_data in sub_scenes_data:
            sub_scene = SubScene(scene_id=scene.id, **sub_data)
            db.add(sub_scene)

    db.commit()
    print(f"Created {len(scenes_data)} scenes")
