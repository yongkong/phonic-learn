"""工单7：学习小结统计——五维完成度与下次复习时间来自后端"""


def test_stats_含五维完成数与下次复习时间(client, registered_user, auth_headers):
    h = auth_headers(registered_user[0])

    # 完成一个词的两个维度
    for dim in ("form", "meaning"):
        res = client.post(
            "/api/v1/learning/complete-dimension",
            json={"word_id": 1, "dimension": dim},
            headers=h,
        )
        assert res.status_code == 200

    stats = client.get("/api/v1/learning/stats", headers=h).json()
    assert stats["dimensions_completed"] == 2
    assert stats["learned_words"] == 1

    # 完词后才有下次复习时间（简化 SM-2：首次 20 分钟后）
    started = client.post(
        "/api/v1/learning/start-session",
        json={"sub_scene_id": 1},
        headers=h,
    ).json()
    client.post(
        "/api/v1/learning/complete-word",
        json={"word_id": 1, "session_id": started["session_id"]},
        headers=h,
    )
    stats = client.get("/api/v1/learning/stats", headers=h).json()
    assert stats["next_review_at"] is not None
    assert stats["dimensions_completed"] == 2  # 完词不新增维度计数


def test_stats_无学习记录时字段为空(client, registered_user, auth_headers):
    stats = client.get(
        "/api/v1/learning/stats", headers=auth_headers(registered_user[0])
    ).json()
    assert stats["dimensions_completed"] == 0
    assert stats["next_review_at"] is None
