"""工单2 AC：音频经端点获取返回 200 且可播放（内容为真实 mp3）"""

from pathlib import Path

from fastapi.testclient import TestClient

# 文件存在性检查针对开发库（与已提交的 static/audios 资产对应）


def test_单词音频端点返回_mp3(client: TestClient):
    res = client.get("/api/v1/audios/words/apple.mp3")
    assert res.status_code == 200
    assert res.headers["content-type"] == "audio/mpeg"
    # 真实音频应有可观长度（Ana 声线最小时长约 2s ≈ 12KB）
    assert len(res.content) > 10000


def test_例句音频端点返回_mp3(client: TestClient):
    res = client.get("/api/v1/audios/sentences/apple_s1.mp3")
    assert res.status_code == 200
    assert res.headers["content-type"] == "audio/mpeg"
    assert len(res.content) > 5000


def test_不存在的音频返回_404(client: TestClient):
    assert client.get("/api/v1/audios/words/nope.mp3").status_code == 404


def test_种子登记的音频文件全部存在():
    """每条登记（词 + 例句）都有对应文件，防止删档/漏生成"""
    import json
    import sqlite3

    from app.config import settings

    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    con = sqlite3.connect(db_path)
    audio_dir = Path("static/audios")
    missing = []
    for spelling, word_audio, sents in con.execute(
        "SELECT spelling, audio_filename, example_sentences FROM words"
    ):
        if word_audio and not (audio_dir / "words" / word_audio).exists():
            missing.append(f"words/{word_audio}")
        for sent in json.loads(sents or "[]"):
            f = sent.get("audio_filename")
            if f and not (audio_dir / "sentences" / f).exists():
                missing.append(f"sentences/{f}")
    assert not missing, f"缺失音频: {missing}"
