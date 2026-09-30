"""学习会话：接口契约（开始/结束会话）"""


def test_end_session_accepts_json_body(client, registered_user, auth_headers):
    """回归：结束会话的参数曾被声明为查询参数，与前端发送 JSON body 的契约不符"""
    token, _ = registered_user
    h = auth_headers(token)

    started = client.post(
        "/api/v1/learning/start-session",
        json={"sub_scene_id": 1, "session_type": "scene_learning"},
        headers=h,
    )
    assert started.status_code == 200
    session_id = started.json()["session_id"]

    resp = client.post(
        "/api/v1/learning/end-session",
        json={"session_id": session_id, "duration_seconds": 120},
        headers=h,
    )
    assert resp.status_code == 200
    assert resp.json()["session_id"] == session_id


def test_end_session_rejects_foreign_session(client, registered_user, auth_headers):
    """别人的会话不能被结束：查不到（非本人）会话时返回 404"""
    token, _ = registered_user
    resp = client.post(
        "/api/v1/learning/end-session",
        json={"session_id": 99999, "duration_seconds": 0},
        headers=auth_headers(token),
    )
    assert resp.status_code == 404
