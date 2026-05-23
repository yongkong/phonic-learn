from datetime import datetime

from pydantic import BaseModel


class MeaningSchema(BaseModel):
    pos: str  # n. / v. / adj. / adv.
    cn: str  # 中文释义


class ExampleSentenceSchema(BaseModel):
    en: str
    cn: str
    audio_filename: str | None = None


class PhonicLetterSound(BaseModel):
    letter: str
    sound: str
    type: str  # vowel / consonant / silent / digraph
    color: str  # red / blue / gray / purple


class PhonicAnalysisSchema(BaseModel):
    syllables: list[str]
    syllable_phonetics: list[str]
    stress_index: int
    letter_sounds: list[PhonicLetterSound]


class MemoryTipSchema(BaseModel):
    type: str  # image / homophone / word-family / action
    content: str


class WordListItem(BaseModel):
    id: int
    spelling: str
    emoji: str | None = None
    phonetic_us: str | None = None
    meanings: list[MeaningSchema]
    image_url: str | None = None
    audio_filename: str | None = None
    learning_status: str = "new"  # new / learning / familiar / mastered
    pronunciation_score: int | None = None

    class Config:
        from_attributes = True


class WordDetailResponse(BaseModel):
    id: int
    spelling: str
    phonetic_us: str | None = None
    phonetic_uk: str | None = None
    meanings: list[MeaningSchema]
    example_sentences: list[ExampleSentenceSchema]
    phonic_analysis: PhonicAnalysisSchema
    memory_tips: list[MemoryTipSchema] | None = None
    image_url: str | None = None
    emoji: str | None = None
    audio_filename: str | None = None
    tags: list[str] | None = None
    grade_range: str

    class Config:
        from_attributes = True


class WordResponse(BaseModel):
    """通用单词响应"""

    id: int
    spelling: str
    phonetic_us: str | None = None
    meanings: list[MeaningSchema]

    class Config:
        from_attributes = True
