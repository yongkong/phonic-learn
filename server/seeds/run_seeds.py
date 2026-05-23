"""种子脚本入口 - 运行此脚本灌入初始数据"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from seeds.seed_scenes import seed_scenes
from seeds.seed_words import seed_words


def run_seeds():
    db = SessionLocal()
    try:
        print("Seeding data...")

        print("\nSeeding scenes...")
        seed_scenes(db)

        print("\nSeeding words...")
        seed_words(db)

        print("\nSeeding completed!")
    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
