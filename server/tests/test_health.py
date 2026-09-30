"""健康检查——验证测试地基本身跑通"""


def test_health_returns_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "app": "WordWorld API"}
