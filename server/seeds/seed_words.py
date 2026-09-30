"""单词种子数据 - MVP 15个测试单词"""

from app.models.scene import SubScene
from app.models.word import Word, SceneWord


def seed_words(db):
    """创建 MVP 测试单词数据"""

    # 检查是否已有数据
    if db.query(Word).first():
        print("Words already exist, skipping")
        return

    words_data = [
        # ===== 厨房 (sub_scene_id=1) =====
        {
            "spelling": "apple",
            "phonetic_us": "/ˈæp.əl/",
            "phonetic_uk": "/ˈæp.əl/",
            "meanings": [{"pos": "n.", "cn": "苹果"}],
            "example_sentences": [
                {"en": "I eat an apple every day.", "cn": "我每天吃一个苹果。"},
                {"en": "The apple is red.", "cn": "苹果是红色的。"},
            ],
            "phonic_analysis": {
                "syllables": ["ap", "ple"],
                "syllable_phonetics": ["/ˈæp/", "/əl/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "a", "sound": "/æ/", "type": "vowel", "color": "red"},
                    {"letter": "p", "sound": "/p/", "type": "consonant", "color": "blue"},
                    {"letter": "p", "sound": "/p/", "type": "consonant", "color": "blue"},
                    {"letter": "l", "sound": "/l/", "type": "consonant", "color": "blue"},
                    {"letter": "e", "sound": "/əl/", "type": "vowel", "color": "red"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🍎 圆圆的苹果，像小球"},
                {"type": "homophone", "content": "apple → 爱剖（剖开吃苹果）"},
            ],
            "emoji": "🍎",
            "audio_filename": "apple.mp3",
            "grade_range": "1-2",
            "tags": ["水果", "食物"],
        },
        {
            "spelling": "bread",
            "phonetic_us": "/bred/",
            "phonetic_uk": "/bred/",
            "meanings": [{"pos": "n.", "cn": "面包"}],
            "example_sentences": [
                {"en": "I have bread for breakfast.", "cn": "我早餐吃面包。"},
            ],
            "phonic_analysis": {
                "syllables": ["bread"],
                "syllable_phonetics": ["/bred/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "b", "sound": "/b/", "type": "consonant", "color": "blue"},
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                    {"letter": "ea", "sound": "/e/", "type": "digraph", "color": "purple"},
                    {"letter": "d", "sound": "/d/", "type": "consonant", "color": "blue"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🍞 一片面包，方方的"},
            ],
            "emoji": "🍞",
            "audio_filename": "bread.mp3",
            "grade_range": "1-2",
            "tags": ["食物", "早餐"],
        },
        {
            "spelling": "milk",
            "phonetic_us": "/mɪlk/",
            "phonetic_uk": "/mɪlk/",
            "meanings": [{"pos": "n.", "cn": "牛奶"}],
            "example_sentences": [
                {"en": "I drink milk before bed.", "cn": "我睡前喝牛奶。"},
            ],
            "phonic_analysis": {
                "syllables": ["milk"],
                "syllable_phonetics": ["/mɪlk/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "m", "sound": "/m/", "type": "consonant", "color": "blue"},
                    {"letter": "i", "sound": "/ɪ/", "type": "vowel", "color": "red"},
                    {"letter": "l", "sound": "/l/", "type": "consonant", "color": "blue"},
                    {"letter": "k", "sound": "/k/", "type": "consonant", "color": "blue"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🥛 一杯白色的牛奶"},
                {"type": "homophone", "content": "milk → 蜜偶渴（喝牛奶解渴）"},
            ],
            "emoji": "🥛",
            "audio_filename": "milk.mp3",
            "grade_range": "1-2",
            "tags": ["饮品", "食物"],
        },
        {
            "spelling": "egg",
            "phonetic_us": "/eɡ/",
            "phonetic_uk": "/eɡ/",
            "meanings": [{"pos": "n.", "cn": "鸡蛋"}],
            "example_sentences": [
                {"en": "I eat an egg for breakfast.", "cn": "我早餐吃一个鸡蛋。"},
            ],
            "phonic_analysis": {
                "syllables": ["egg"],
                "syllable_phonetics": ["/eɡ/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "e", "sound": "/e/", "type": "vowel", "color": "red"},
                    {"letter": "g", "sound": "/ɡ/", "type": "consonant", "color": "blue"},
                    {"letter": "g", "sound": "/ɡ/", "type": "consonant", "color": "blue"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🥚 椭圆形的鸡蛋"},
            ],
            "emoji": "🥚",
            "audio_filename": "egg.mp3",
            "grade_range": "1-2",
            "tags": ["食物", "早餐"],
        },
        {
            "spelling": "rice",
            "phonetic_us": "/raɪs/",
            "phonetic_uk": "/raɪs/",
            "meanings": [{"pos": "n.", "cn": "米饭"}],
            "example_sentences": [
                {"en": "I eat rice for lunch.", "cn": "我午餐吃米饭。"},
            ],
            "phonic_analysis": {
                "syllables": ["rice"],
                "syllable_phonetics": ["/raɪs/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                    {"letter": "i", "sound": "/aɪ/", "type": "vowel", "color": "red"},
                    {"letter": "c", "sound": "/s/", "type": "consonant", "color": "blue"},
                    {"letter": "e", "sound": "", "type": "silent", "color": "gray"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🍚 一碗白白的米饭"},
            ],
            "emoji": "🍚",
            "audio_filename": "rice.mp3",
            "grade_range": "1-2",
            "tags": ["食物", "主食"],
        },
        # ===== 教室 (sub_scene_id=3) =====
        {
            "spelling": "book",
            "phonetic_us": "/bʊk/",
            "phonetic_uk": "/bʊk/",
            "meanings": [{"pos": "n.", "cn": "书"}],
            "example_sentences": [
                {"en": "I read a book.", "cn": "我读一本书。"},
                {"en": "Open your book.", "cn": "打开你的书。"},
            ],
            "phonic_analysis": {
                "syllables": ["book"],
                "syllable_phonetics": ["/bʊk/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "b", "sound": "/b/", "type": "consonant", "color": "blue"},
                    {"letter": "oo", "sound": "/ʊ/", "type": "digraph", "color": "purple"},
                    {"letter": "k", "sound": "/k/", "type": "consonant", "color": "blue"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "📖 一本书，可以翻开"},
            ],
            "emoji": "📖",
            "audio_filename": "book.mp3",
            "grade_range": "1-2",
            "tags": ["学习用品", "学校"],
        },
        {
            "spelling": "pen",
            "phonetic_us": "/pen/",
            "phonetic_uk": "/pen/",
            "meanings": [{"pos": "n.", "cn": "钢笔"}],
            "example_sentences": [
                {"en": "I write with a pen.", "cn": "我用钢笔写字。"},
            ],
            "phonic_analysis": {
                "syllables": ["pen"],
                "syllable_phonetics": ["/pen/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "p", "sound": "/p/", "type": "consonant", "color": "blue"},
                    {"letter": "e", "sound": "/e/", "type": "vowel", "color": "red"},
                    {"letter": "n", "sound": "/n/", "type": "consonant", "color": "blue"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "✏️ 一支笔，可以写字"},
            ],
            "emoji": "✏️",
            "audio_filename": "pen.mp3",
            "grade_range": "1-2",
            "tags": ["学习用品", "学校"],
        },
        {
            "spelling": "desk",
            "phonetic_us": "/desk/",
            "phonetic_uk": "/desk/",
            "meanings": [{"pos": "n.", "cn": "书桌"}],
            "example_sentences": [
                {"en": "My book is on the desk.", "cn": "我的书在书桌上。"},
            ],
            "phonic_analysis": {
                "syllables": ["desk"],
                "syllable_phonetics": ["/desk/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "d", "sound": "/d/", "type": "consonant", "color": "blue"},
                    {"letter": "e", "sound": "/e/", "type": "vowel", "color": "red"},
                    {"letter": "s", "sound": "/s/", "type": "consonant", "color": "blue"},
                    {"letter": "k", "sound": "/k/", "type": "consonant", "color": "blue"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🪑 一张书桌，可以放书"},
            ],
            "emoji": "🪑",
            "audio_filename": "desk.mp3",
            "grade_range": "1-2",
            "tags": ["家具", "学校"],
        },
        {
            "spelling": "teacher",
            "phonetic_us": "/ˈtiː.tʃər/",
            "phonetic_uk": "/ˈtiː.tʃə/",
            "meanings": [{"pos": "n.", "cn": "老师"}],
            "example_sentences": [
                {"en": "My teacher is kind.", "cn": "我的老师很和蔼。"},
            ],
            "phonic_analysis": {
                "syllables": ["tea", "cher"],
                "syllable_phonetics": ["/ˈtiː/", "/tʃər/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "t", "sound": "/t/", "type": "consonant", "color": "blue"},
                    {"letter": "ea", "sound": "/iː/", "type": "digraph", "color": "purple"},
                    {"letter": "ch", "sound": "/tʃ/", "type": "digraph", "color": "purple"},
                    {"letter": "e", "sound": "/ə/", "type": "vowel", "color": "red"},
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "👩‍🏫 一位老师在教书"},
                {"type": "word-family", "content": "teach (教) + er (人) = teacher (老师)"},
            ],
            "emoji": "👩‍🏫",
            "audio_filename": "teacher.mp3",
            "grade_range": "1-2",
            "tags": ["人物", "学校"],
        },
        {
            "spelling": "classroom",
            "phonetic_us": "/ˈklæs.ruːm/",
            "phonetic_uk": "/ˈklɑːs.ruːm/",
            "meanings": [{"pos": "n.", "cn": "教室"}],
            "example_sentences": [
                {"en": "We study in the classroom.", "cn": "我们在教室里学习。"},
            ],
            "phonic_analysis": {
                "syllables": ["class", "room"],
                "syllable_phonetics": ["/ˈklæs/", "/ruːm/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "c", "sound": "/k/", "type": "consonant", "color": "blue"},
                    {"letter": "l", "sound": "/l/", "type": "consonant", "color": "blue"},
                    {"letter": "a", "sound": "/æ/", "type": "vowel", "color": "red"},
                    {"letter": "ss", "sound": "/s/", "type": "consonant", "color": "blue"},
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                    {"letter": "oo", "sound": "/uː/", "type": "digraph", "color": "purple"},
                    {"letter": "m", "sound": "/m/", "type": "consonant", "color": "blue"},
                ],
            },
            "memory_tips": [
                {"type": "word-family", "content": "class (班级) + room (房间) = classroom (教室)"},
            ],
            "emoji": "🏫",
            "audio_filename": "classroom.mp3",
            "grade_range": "1-2",
            "tags": ["地点", "学校"],
        },
        # ===== 水果区 (sub_scene_id=5) =====
        {
            "spelling": "orange",
            "phonetic_us": "/ˈɒr.ɪndʒ/",
            "phonetic_uk": "/ˈɔːr.ɪndʒ/",
            "meanings": [
                {"pos": "n.", "cn": "橙子；橘子"},
                {"pos": "adj.", "cn": "橙色的"},
            ],
            "example_sentences": [
                {"en": "I like to eat an orange.", "cn": "我喜欢吃橙子。"},
                {"en": "The orange cat is sleeping.", "cn": "那只橙色的猫正在睡觉。"},
            ],
            "phonic_analysis": {
                "syllables": ["o", "range"],
                "syllable_phonetics": ["/ˈɒ/", "/rɪndʒ/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "o", "sound": "/ɒ/", "type": "vowel", "color": "red"},
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                    {"letter": "a", "sound": "/ɪ/", "type": "vowel", "color": "red"},
                    {"letter": "n", "sound": "/n/", "type": "consonant", "color": "blue"},
                    {"letter": "ge", "sound": "/dʒ/", "type": "digraph", "color": "purple"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🍊 圆圆的橙子，像太阳一样"},
                {"type": "homophone", "content": "orange → 偶润橘（水润的橘子）"},
            ],
            "emoji": "🍊",
            "audio_filename": "orange.mp3",
            "grade_range": "1-2",
            "tags": ["水果", "颜色"],
        },
        {
            "spelling": "banana",
            "phonetic_us": "/bəˈnæn.ə/",
            "phonetic_uk": "/bəˈnɑː.nə/",
            "meanings": [{"pos": "n.", "cn": "香蕉"}],
            "example_sentences": [
                {"en": "Monkeys like bananas.", "cn": "猴子喜欢香蕉。"},
            ],
            "phonic_analysis": {
                "syllables": ["ba", "na", "na"],
                "syllable_phonetics": ["/bə/", "/ˈnæn/", "/ə/"],
                "stress_index": 1,
                "letter_sounds": [
                    {"letter": "b", "sound": "/b/", "type": "consonant", "color": "blue"},
                    {"letter": "a", "sound": "/ə/", "type": "vowel", "color": "red"},
                    {"letter": "n", "sound": "/n/", "type": "consonant", "color": "blue"},
                    {"letter": "a", "sound": "/æ/", "type": "vowel", "color": "red"},
                    {"letter": "n", "sound": "/n/", "type": "consonant", "color": "blue"},
                    {"letter": "a", "sound": "/ə/", "type": "vowel", "color": "red"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🍌 弯弯的香蕉，像月亮"},
            ],
            "emoji": "🍌",
            "audio_filename": "banana.mp3",
            "grade_range": "1-2",
            "tags": ["水果"],
        },
        {
            "spelling": "grape",
            "phonetic_us": "/ɡreɪp/",
            "phonetic_uk": "/ɡreɪp/",
            "meanings": [{"pos": "n.", "cn": "葡萄"}],
            "example_sentences": [
                {"en": "I like grapes.", "cn": "我喜欢葡萄。"},
            ],
            "phonic_analysis": {
                "syllables": ["grape"],
                "syllable_phonetics": ["/ɡreɪp/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "g", "sound": "/ɡ/", "type": "consonant", "color": "blue"},
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                    {"letter": "a", "sound": "/eɪ/", "type": "vowel", "color": "red"},
                    {"letter": "p", "sound": "/p/", "type": "consonant", "color": "blue"},
                    {"letter": "e", "sound": "", "type": "silent", "color": "gray"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🍇 一串紫色的葡萄"},
            ],
            "emoji": "🍇",
            "audio_filename": "grape.mp3",
            "grade_range": "1-2",
            "tags": ["水果"],
        },
        {
            "spelling": "strawberry",
            "phonetic_us": "/ˈstrɔː.ber.i/",
            "phonetic_uk": "/ˈstrɔː.bər.i/",
            "meanings": [{"pos": "n.", "cn": "草莓"}],
            "example_sentences": [
                {"en": "Strawberry is sweet.", "cn": "草莓很甜。"},
            ],
            "phonic_analysis": {
                "syllables": ["straw", "ber", "ry"],
                "syllable_phonetics": ["/ˈstrɔː/", "/ber/", "/i/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "s", "sound": "/s/", "type": "consonant", "color": "blue"},
                    {"letter": "t", "sound": "/t/", "type": "consonant", "color": "blue"},
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                    {"letter": "aw", "sound": "/ɔː/", "type": "digraph", "color": "purple"},
                    {"letter": "b", "sound": "/b/", "type": "consonant", "color": "blue"},
                    {"letter": "e", "sound": "/e/", "type": "vowel", "color": "red"},
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                    {"letter": "r", "sound": "/r/", "type": "consonant", "color": "blue"},
                    {"letter": "y", "sound": "/i/", "type": "vowel", "color": "red"},
                ],
            },
            "memory_tips": [
                {"type": "word-family", "content": "straw (稻草) + berry (浆果) = strawberry (草莓)"},
            ],
            "emoji": "🍓",
            "audio_filename": "strawberry.mp3",
            "grade_range": "2-3",
            "tags": ["水果"],
        },
        {
            "spelling": "peach",
            "phonetic_us": "/piːtʃ/",
            "phonetic_uk": "/piːtʃ/",
            "meanings": [{"pos": "n.", "cn": "桃子"}],
            "example_sentences": [
                {"en": "The peach is pink.", "cn": "桃子是粉色的。"},
            ],
            "phonic_analysis": {
                "syllables": ["peach"],
                "syllable_phonetics": ["/piːtʃ/"],
                "stress_index": 0,
                "letter_sounds": [
                    {"letter": "p", "sound": "/p/", "type": "consonant", "color": "blue"},
                    {"letter": "ea", "sound": "/iː/", "type": "digraph", "color": "purple"},
                    {"letter": "ch", "sound": "/tʃ/", "type": "digraph", "color": "purple"},
                ],
            },
            "memory_tips": [
                {"type": "image", "content": "🍑 粉色的桃子，像心形"},
            ],
            "emoji": "🍑",
            "audio_filename": "peach.mp3",
            "grade_range": "1-2",
            "tags": ["水果"],
        },
    ]

    # 单词和子场景的映射：按子场景名称（域概念）关联，
    # 不依赖自增 id 的插入顺序——顺序变化不会再导致映射静默错位
    word_to_sub_scene_name = {
        "apple": "厨房", "bread": "厨房", "milk": "厨房", "egg": "厨房", "rice": "厨房",
        "book": "教室", "pen": "教室", "desk": "教室", "teacher": "教室", "classroom": "教室",
        "orange": "水果区", "banana": "水果区", "grape": "水果区",
        "strawberry": "水果区", "peach": "水果区",
    }

    name_to_id = {ss.name: ss.id for ss in db.query(SubScene).all()}
    missing = set(word_to_sub_scene_name.values()) - set(name_to_id)
    if missing:
        raise ValueError(f"种子引用了不存在的子场景: {sorted(missing)}")

    words_created = 0
    for word_data in words_data:
        # 例句音频按约定登记：{spelling}_s{n}.mp3，与 gen_audios.py 的
        # 生成命名一致；音频文件本身由该脚本幂等补齐
        for idx, sentence in enumerate(word_data["example_sentences"], start=1):
            sentence.setdefault(
                "audio_filename", f"{word_data['spelling']}_s{idx}.mp3"
            )
        word = Word(**word_data)
        db.add(word)
        db.flush()

        # 创建场景-单词关联
        sub_scene_id = name_to_id[word_to_sub_scene_name[word_data["spelling"]]]
        scene_word = SceneWord(
            sub_scene_id=sub_scene_id,
            word_id=word.id,
            sort_order=words_created,
        )
        db.add(scene_word)
        words_created += 1

    db.commit()
    print(f"Created {words_created} words")
