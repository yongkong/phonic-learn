"""场景与词表：种子数据经 API 可见"""


def _get_scene(scenes, name):
    return next(s for s in scenes if s["name"] == name)


def test_scenes_list_returns_seeded_scenes(client, registered_user, auth_headers):
    token, _ = registered_user
    resp = client.get("/api/v1/scenes", headers=auth_headers(token))
    assert resp.status_code == 200
    scenes = resp.json()
    assert [s["name"] for s in scenes] == ["我的家", "我的学校", "超市购物"]

    home = _get_scene(scenes, "我的家")
    assert [ss["name"] for ss in home["sub_scenes"]] == ["厨房", "客厅"]
    assert home["sub_scenes"][0]["word_count"] == 5  # 厨房 5 词
    assert home["sub_scenes"][1]["word_count"] == 0  # 客厅暂无词

    school = _get_scene(scenes, "我的学校")
    assert school["sub_scenes"][0]["word_count"] == 5  # 教室 5 词


def test_fruit_area_lists_five_words(client, registered_user, auth_headers):
    """回归：水果词曾映射到不存在的子场景 id，导致水果区词表为空"""
    token, _ = registered_user
    scenes = client.get("/api/v1/scenes", headers=auth_headers(token)).json()
    market = _get_scene(scenes, "超市购物")
    fruit = next(ss for ss in market["sub_scenes"] if ss["name"] == "水果区")

    assert fruit["word_count"] == 5

    resp = client.get(
        f"/api/v1/words/sub-scenes/{fruit['id']}/words",
        headers=auth_headers(token),
    )
    assert resp.status_code == 200
    words = resp.json()
    assert sorted(w["spelling"] for w in words) == [
        "banana",
        "grape",
        "orange",
        "peach",
        "strawberry",
    ]
    # 新用户对所有词都是"新学"状态
    assert all(w["learning_status"] == "new" for w in words)


def test_scene_detail_returns_404_for_unknown_id(client, registered_user, auth_headers):
    """回归：不存在的场景 id 曾因缺少 HTTPException 导入而返回 500"""
    token, _ = registered_user
    resp = client.get("/api/v1/scenes/99999", headers=auth_headers(token))
    assert resp.status_code == 404
