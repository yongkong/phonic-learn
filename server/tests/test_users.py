"""用户接口：注册发放 token、获取当前用户"""


def test_register_issues_token_and_user(client):
    resp = client.post(
        "/api/v1/users/register",
        json={"nickname": "小明", "grade": 2},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["nickname"] == "小明"
    assert data["grade"] == 2
    # 无密码账号：注册即发 token（ADR-0004）
    assert isinstance(data["token"], str) and len(data["token"]) >= 32


def test_register_rejects_duplicate_nickname(client):
    body = {"nickname": "重复昵称同学", "grade": 1}
    assert client.post("/api/v1/users/register", json=body).status_code == 200
    assert client.post("/api/v1/users/register", json=body).status_code == 409


def test_register_rejects_invalid_grade(client):
    resp = client.post(
        "/api/v1/users/register",
        json={"nickname": "年级越界", "grade": 7},
    )
    assert resp.status_code == 422


def test_me_returns_current_user(client, registered_user, auth_headers):
    token, user = registered_user
    resp = client.get("/api/v1/users/me", headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["id"] == user["id"]
    assert resp.json()["nickname"] == user["nickname"]


def test_me_rejects_missing_token(client):
    assert client.get("/api/v1/users/me").status_code == 422
    assert (
        client.get(
            "/api/v1/users/me", headers={"Authorization": "Bearer not-a-token"}
        ).status_code
        == 401
    )
