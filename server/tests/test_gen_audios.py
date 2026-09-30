"""工单2：音频生成脚本的收集逻辑（幂等：存在的跳过、缺失的补齐）"""

import json
from pathlib import Path

from seeds.gen_audios import collect_audios_to_generate


def _word(spelling, audio_filename, sentences):
    return {
        "spelling": spelling,
        "audio_filename": audio_filename,
        "example_sentences": json.dumps(sentences),
    }


def test_无音频目录时全部待生成(tmp_path: Path):
    rows = [
        _word("apple", "apple.mp3", [{"en": "I eat an apple.", "audio_filename": "apple_s1.mp3"}]),
    ]
    tasks = collect_audios_to_generate(rows, tmp_path)
    kinds = sorted((t.kind, t.filename) for t in tasks)
    assert kinds == [
        ("sentences", "apple_s1.mp3"),
        ("words", "apple.mp3"),
    ]
    assert tasks[0].text and tasks[1].text


def test_已存在的音频被跳过_缺失的补齐(tmp_path: Path):
    (tmp_path / "words").mkdir()
    (tmp_path / "words" / "apple.mp3").write_bytes(b"existing")
    rows = [
        _word("apple", "apple.mp3", [{"en": "I eat an apple.", "audio_filename": "apple_s1.mp3"}]),
    ]
    tasks = collect_audios_to_generate(rows, tmp_path)
    assert [t.filename for t in tasks] == ["apple_s1.mp3"]


def test_例句缺_audio_filename_登记时跳过并计数(tmp_path: Path):
    rows = [
        _word("apple", "apple.mp3", [{"en": "I eat an apple."}]),
    ]
    tasks = collect_audios_to_generate(rows, tmp_path)
    # 单词生成，例句未登记文件名 → 不生成（登记属种子职责）
    assert [t.filename for t in tasks] == ["apple.mp3"]


def test_同名单词与例句互不冲突(tmp_path: Path):
    rows = [
        _word("egg", "egg.mp3", [{"en": "I eat an egg.", "audio_filename": "egg_s1.mp3"}]),
    ]
    tasks = collect_audios_to_generate(rows, tmp_path)
    paths = {t.out_path for t in tasks}
    assert len(paths) == 2
