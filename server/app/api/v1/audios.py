from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter(prefix="/audios", tags=["audios"])


@router.get("/words/{filename}", summary="获取单词发音音频")
def get_word_audio(filename: str):
    """获取单词发音音频文件"""
    audio_path = Path(settings.AUDIO_DIR) / "words" / filename

    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="音频文件不存在")

    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename=filename,
    )


@router.get("/sentences/{filename}", summary="获取例句音频")
def get_sentence_audio(filename: str):
    """获取例句音频文件"""
    audio_path = Path(settings.AUDIO_DIR) / "sentences" / filename

    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="音频文件不存在")

    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename=filename,
    )
