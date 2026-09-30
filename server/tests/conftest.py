"""测试地基：独立临时数据库 + 种子数据 + TestClient

接缝约定（见规格 Issue #1）：所有测试只打 HTTP API，
不触碰内部实现；数据库使用临时文件，不影响开发库。
"""

import atexit
import os
import tempfile
import uuid
from pathlib import Path

# 配置在导入时读取环境变量，必须先于 app 的任何导入执行。
# 每轮 pytest 使用唯一文件名（避免同机并发互删）；
# 防重入守卫防止 conftest 被以不同模块名重复导入时重复执行。
if not os.environ.get("WORDWORLD_TEST_DB_READY"):
    _TEST_DB = Path(tempfile.gettempdir()) / f"wordworld_test_{uuid.uuid4().hex[:8]}.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB.as_posix()}"
    os.environ["WORDWORLD_TEST_DB_READY"] = "1"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.database import SessionLocal, engine  # noqa: E402
from seeds.seed_scenes import seed_scenes  # noqa: E402
from seeds.seed_words import seed_words  # noqa: E402


def _cleanup_test_db():
    """进程退出时尽力清理临时库：先释放连接池，再删文件"""
    engine.dispose()
    try:
        _TEST_DB.unlink(missing_ok=True)
    except PermissionError:
        pass  # 文件仍被占用则留给系统临时目录清理


atexit.register(_cleanup_test_db)


def _run_seeds():
    db = SessionLocal()
    try:
        seed_scenes(db)
        seed_words(db)
    finally:
        db.close()


_run_seeds()


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def registered_user(client):
    """注册一个全新用户，返回 (token, 用户信息字典)"""
    nickname = f"测试学生-{uuid.uuid4().hex[:8]}"
    resp = client.post(
        "/api/v1/users/register",
        json={"nickname": nickname, "grade": 3},
    )
    assert resp.status_code == 200
    data = resp.json()
    return data["token"], data


@pytest.fixture
def auth_headers():
    """返回构造 Bearer 认证头的函数（不以 import 方式共享，避免 conftest 被重复导入）"""

    def _make(token):
        return {"Authorization": f"Bearer {token}"}

    return _make
