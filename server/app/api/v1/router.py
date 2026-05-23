from fastapi import APIRouter

from app.api.v1.users import router as users_router
from app.api.v1.scenes import router as scenes_router
from app.api.v1.words import router as words_router
from app.api.v1.learning import router as learning_router
from app.api.v1.audios import router as audios_router

router = APIRouter(prefix="/api/v1")

# Include all routers
router.include_router(users_router)
router.include_router(scenes_router)
router.include_router(words_router)
router.include_router(learning_router)
router.include_router(audios_router)
