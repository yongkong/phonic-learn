"""音频资产管线：用 edge-tts 为种子单词与例句批量生成 mp3。

幂等：已存在的音频跳过、缺失的补齐；将来扩词后重跑同一脚本即可。
用法：python seeds/gen_audios.py [--dry-run]
"""

import argparse
import asyncio
import json
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 儿童产品：Ana 是美式儿童声线，语速略放慢便于跟读
VOICE = "en-US-AnaNeural"
RATE = "-8%"

STATIC_DIR = Path(__file__).parent.parent / "static" / "audios"


@dataclass(frozen=True)
class AudioTask:
    """一条待生成的音频：text → static/audios/{kind}/{filename}"""

    text: str
    kind: str  # words | sentences
    filename: str

    @property
    def out_path(self) -> Path:
        return STATIC_DIR / self.kind / self.filename


def collect_audios_to_generate(word_rows, audio_dir: Path) -> list[AudioTask]:
    """对比数据库登记与磁盘文件，返回缺失的音频任务。

    word_rows: 含 spelling / audio_filename / example_sentences(JSON 文本) 的行
    audio_dir: static/audios 目录（生产环境用模块级 STATIC_DIR，测试注入临时目录）
    """
    tasks: list[AudioTask] = []

    for row in word_rows:
        word_audio = row["audio_filename"]
        if word_audio and not (audio_dir / "words" / word_audio).exists():
            tasks.append(AudioTask(row["spelling"], "words", word_audio))

        sentences = json.loads(row["example_sentences"] or "[]")
        for sent in sentences:
            sent_audio = sent.get("audio_filename")
            # 例句未登记文件名时跳过：登记属种子数据职责，不在此处推断
            if sent_audio and not (audio_dir / "sentences" / sent_audio).exists():
                tasks.append(AudioTask(sent["en"], "sentences", sent_audio))

    return tasks


def _fetch_rows():
    from app.database import SessionLocal
    from sqlalchemy import text

    db = SessionLocal()
    try:
        return db.execute(
            text("SELECT spelling, audio_filename, example_sentences FROM words ORDER BY id")
        ).mappings().all()
    finally:
        db.close()


async def _generate(task: AudioTask) -> None:
    import edge_tts

    task.out_path.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(task.text, VOICE, rate=RATE)
    await communicate.save(str(task.out_path))


async def _run(dry_run: bool) -> None:
    rows = _fetch_rows()
    tasks = collect_audios_to_generate(rows, STATIC_DIR)
    print(f"共 {len(tasks)} 条音频待生成（已存在的已跳过）")
    if dry_run:
        for t in tasks:
            print(f"  [dry-run] {t.kind}/{t.filename}: {t.text}")
        return
    for t in tasks:
        await _generate(t)
        print(f"  generated {t.kind}/{t.filename}")
    print(f"完成：{len(tasks)} 条音频已生成")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="只列出待生成项")
    args = parser.parse_args()
    asyncio.run(_run(args.dry_run))


if __name__ == "__main__":
    main()
