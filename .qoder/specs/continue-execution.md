# WordWorld MVP Phase 1 — 继续执行计划

## Context

WordWorld 小学英语单词记忆 App 已完成完整的设计阶段（设计文档、CSS tokens、UI 原型图）。后端已完成 Step 1 项目初始化（requirements.txt、config.py、database.py、main.py、run.py），但缺少数据库模型等关键文件。`app/` 目录仍为空，需要初始化 unibest 项目。

**当前进度：** 后端 Step 1 完成 60%（基础脚手架完成，缺少 models/、schemas/、api/、services/ 目录和文件）

**实施策略：** 采用"后端优先"策略，先建立 FastAPI 后端基础（数据库模型 + API），再初始化 unibest 前端并对接。这样前端开发时有真实 API 可用。

**技术栈：**
- 前端：unibest (uni-app + Vue3 + TypeScript) + wot-design-uni + Pinia
- 后端：FastAPI (Python) + SQLite + SQLAlchemy
- 认证：简化 token 方案（注册即生成 UUID）

**MVP 范围：** 用户注册 + 年级选择、3个场景地图、五维学习卡片、发音播放、跟读评分、拼写练习、学习进度记录

---

## 实施步骤

### Phase 1: 后端基础 (FastAPI + SQLite)

#### Step 1: 项目初始化
- 创建 `server/requirements.txt` (fastapi, uvicorn, sqlalchemy, pydantic, pydantic-settings, alembic, python-multipart)
- 创建 `server/.env.example` (DATABASE_URL, DEBUG, CORS_ORIGINS)
- 创建 `server/app/__init__.py`
- 创建 `server/app/config.py` (Pydantic Settings 读取环境变量)
- 创建 `server/app/database.py` (SQLite engine + SessionLocal)
- 创建 `server/app/main.py` (FastAPI app + CORS + 健康检查 `/health`)
- 创建 `server/run.py` (uvicorn 启动脚本)

**验证：** `cd server && python run.py` 启动后访问 `http://localhost:8000/docs` 看到 Swagger UI

#### Step 2: 数据库模型 (SQLAlchemy)
- 创建 `server/app/models/__init__.py` (导出所有模型)
- 创建 `server/app/models/user.py` (users 表：id, nickname, grade, token, created_at, updated_at)
- 创建 `server/app/models/scene.py` (scenes + sub_scenes 表)
- 创建 `server/app/models/word.py` (words 表 + scene_words 关联表)
- 创建 `server/app/models/learning_record.py` (learning_records + learning_sessions 表)

**关键字段：**
- `words.meanings` / `phonic_analysis` / `memory_tips` / `example_sentences` 使用 JSON 类型
- `learning_records.dimension_progress` 使用 JSON 存储五维进度
- `learning_records.next_review_at` / `ease_factor` / `repetition_count` 支持后续艾宾浩斯复习

#### Step 3: 数据库迁移 (Alembic)
- 初始化 alembic：`cd server && alembic init alembic`
- 配置 `alembic.ini` 读取 `.env` 中的 DATABASE_URL
- 配置 `alembic/env.py` 导入所有 models
- 生成迁移：`alembic revision --autogenerate -m "initial tables"`
- 执行迁移：`alembic upgrade head`

#### Step 4: Pydantic Schemas
- 创建 `server/app/schemas/__init__.py`
- 创建 `server/app/schemas/user.py` (RegisterRequest, UserResponse, UserStatsResponse)
- 创建 `server/app/schemas/scene.py` (SceneResponse, SubSceneResponse)
- 创建 `server/app/schemas/word.py` (WordResponse, WordListItem, MeaningSchema, PhonicAnalysisSchema)
- 创建 `server/app/schemas/learning.py` (CompleteDimensionRequest, CompleteWordRequest, LearningStatsResponse)

#### Step 5: API 依赖注入
- 创建 `server/app/api/__init__.py`
- 创建 `server/app/api/deps.py` (get_db, get_current_user)

#### Step 6: 用户 API
- 创建 `server/app/api/v1/__init__.py`
- 创建 `server/app/api/v1/users.py` (register, get_me, get_stats)
- 创建 `server/app/api/v1/router.py` (聚合 v1 路由)

#### Step 7: 场景 + 单词 API
- 创建 `server/app/api/v1/scenes.py` (GET /scenes, GET /scenes/{id})
- 创建 `server/app/api/v1/words.py` (GET /sub-scenes/{id}/words, GET /words/{id})

#### Step 8: 学习记录 API
- 创建 `server/app/services/__init__.py`
- 创建 `server/app/services/learning_service.py` (start_session, complete_dimension, complete_word, record_pronunciation, end_session)
- 创建 `server/app/api/v1/learning.py` (学习记录路由)

#### Step 9: 音频服务
- 创建 `server/static/audios/words/` 目录
- 创建 `server/app/api/v1/audios.py` (音频文件服务)

#### Step 10: 种子数据
- 创建 `server/seeds/__init__.py`
- 创建 `server/seeds/seed_scenes.py` (3个场景 + 子场景)
- 创建 `server/seeds/seed_words.py` (15个测试单词 + 完整五维数据)
- 创建 `server/seeds/run_seeds.py` (种子脚本入口)

---

### Phase 2: 前端基础设施 (unibest)

#### Step 11: unibest 项目初始化
- 执行 `cd app && pnpm create unibest@latest .` (选择 TypeScript, Vue3, Vite, pnpm)
- 安装额外依赖：`pnpm add wot-design-uni pinia pinia-plugin-persistedstate sass`

#### Step 12: 设计系统集成
- 转换 `design/css/tokens.css` → `app/src/styles/tokens.scss`
- 创建 `app/src/styles/mixins.scss`
- 创建 `app/src/styles/common.scss`
- 配置 `vite.config.ts` 自动注入 tokens.scss
- 更新 `app/src/App.vue` 引入全局样式

#### Step 13: 路由配置
- 创建所有页面目录：`pages/{splash,onboarding,register,home,scene,learn,summary,practice,essay,profile}/index.vue`
- 配置 `app/src/pages.json` (路由 + TabBar)
- 创建占位页面内容

#### Step 14: TypeScript 类型定义
- 创建 `app/src/types/user.ts`
- 创建 `app/src/types/scene.ts`
- 创建 `app/src/types/word.ts`
- 创建 `app/src/types/learning.ts`

#### Step 15: Pinia Stores
- 创建 `app/src/stores/user.ts` (用户信息 + 持久化)
- 创建 `app/src/stores/scene.ts` (场景数据)
- 创建 `app/src/stores/progress.ts` (学习进度 + 持久化)
- 创建 `app/src/stores/learn.ts` (当前学习会话)

#### Step 16: API 层
- 创建 `app/src/api/request.ts` (uni.request 封装 + token 注入)
- 创建 `app/src/api/user.ts`
- 创建 `app/src/api/scene.ts`
- 创建 `app/src/api/word.ts`
- 创建 `app/src/api/learning.ts`

#### Step 17: 工具函数
- 创建 `app/src/utils/storage.ts` (本地存储封装)
- 创建 `app/src/utils/letter.ts` (彩色字母标注逻辑)
- 创建 `app/src/utils/audio.ts` (音频播放/录制)
- 创建 `app/src/utils/format.ts` (格式化函数)

---

### Phase 3: 核心功能实现

#### Step 18: 公共组件
- 创建 `app/src/components/common/NavBar.vue`
- 创建 `app/src/components/common/TabBar.vue` (或使用 wot-design-uni tabBar)
- 创建 `app/src/components/common/ProgressBar.vue`
- 创建 `app/src/components/word/WordDisplay.vue` ⭐ (彩色字母标注核心组件)
- 创建 `app/src/components/word/WordCard.vue`
- 创建 `app/src/components/word/LetterTile.vue`

#### Step 19: 引导 + 注册流程
- 实现 `app/src/pages/splash/index.vue` (启动页 + 自动跳转)
- 实现 `app/src/pages/onboarding/index.vue` (3屏引导 + wd-swiper)
- 实现 `app/src/pages/register/index.vue` (昵称输入 + 年级选择)
- 实现路由守卫 (检查 isOnboarded 和 grade)

#### Step 20: 场景地图主页
- 实现 `app/src/pages/home/index.vue`
- 创建 `app/src/components/scene/SceneCard.vue`
- 创建 `app/src/components/scene/SceneMapPath.vue`
- 对接后端场景 API

#### Step 21: 场景单词列表
- 实现 `app/src/pages/scene/index.vue`
- 实现 `app/src/components/word/WordCard.vue` (已学/当前/锁定状态)

#### Step 22: 五维学习核心 ⭐
- 创建 `app/src/composables/useLearnFlow.ts` (学习流程状态机)
- 创建 `app/src/composables/useAudio.ts` (音频播放 hook)
- 创建 `app/src/composables/useSpeakScore.ts` (跟读评分 hook)
- 实现 `app/src/pages/learn/index.vue` (学习页框架)
- 创建 `app/src/components/learn/DimensionStepBar.vue`
- 创建 `app/src/components/learn/DimensionForm.vue` (第①维：形)
- 创建 `app/src/components/learn/DimensionMeaning.vue` (第②维：义)
- 创建 `app/src/components/learn/DimensionSound.vue` (第③维：音)
- 创建 `app/src/components/learn/DimensionMemory.vue` (第④维：记)
- 创建 `app/src/components/learn/DimensionUsage.vue` (第⑤维：用)
- 创建 `app/src/components/learn/SpeakButton.vue` (跟读按钮)
- 创建 `app/src/components/game/SpellInput.vue` (拼写输入)
- 创建 `app/src/components/game/FillBlank.vue` (填空练习)

#### Step 23: 学习小结
- 实现 `app/src/pages/summary/index.vue`

#### Step 24: 个人中心
- 实现 `app/src/pages/profile/index.vue`

#### Step 25: 占位页面
- 实现 `app/src/pages/practice/index.vue` ("Coming Soon")
- 实现 `app/src/pages/essay/index.vue` ("Coming Soon")

---

## 验证方案

### 后端验证
1. `cd server && python run.py` → 访问 `http://localhost:8000/docs`
2. Swagger UI 测试完整流程：注册 → 获取 token → 场景列表 → 单词列表 → 开始学习 → 完成维度 → 完成单词 → 统计
3. 检查 SQLite 数据库表结构和种子数据

### 前端验证
1. `cd app && pnpm dev:h5` → H5 模式测试
2. 完整流程：启动 → 注册 → 选场景 → 学单词 (五维) → 小结 → 个人中心
3. 检查彩色字母标注、音频播放、跟读录音
4. 检查本地存储持久化

---

## 关键文件

- `server/app/database.py` — 数据库引擎和 Session 管理
- `server/app/models/learning_record.py` — 学习记录模型 (含艾宾浩斯字段)
- `server/app/services/learning_service.py` — 学习业务逻辑 (五维流程 + SM-2 算法)
- `server/seeds/seed_words.py` — 15个测试单词的完整五维数据
- `app/src/pages/learn/index.vue` — 五维学习核心页面
- `app/src/components/word/WordDisplay.vue` — 彩色字母标注核心组件
- `app/src/composables/useLearnFlow.ts` — 学习流程状态机
- `app/src/utils/letter.ts` — 字母类型分析工具
