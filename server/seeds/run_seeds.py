"""种子脚本入口 - 运行此脚本灌入初始数据"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, Base, engine

# 建表逻辑在 app.main 导入时执行；单独运行种子脚本时需要先自行建表，
# 否则全新的开发库会因表不存在而失败
from app.models import user, scene, word, learning_record  # noqa: F401
Base.metadata.create_all(bind=engine)

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
