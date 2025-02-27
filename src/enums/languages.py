from enum import Enum


class Language(Enum):
    PT = "pt"
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    IT = "it"
    RU = "ru"
    JA = "ja"
    KO = "ko"
    ZH = "zh"

    __LANGUAGE_NAMES = {
        "pt": "Portuguese",
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese (Mandarin)",
    }

    @staticmethod
    def get_fullname_language(lang: str):
        return Language.__LANGUAGE_NAMES[lang]

    @staticmethod
    def get_available_languages():
        return Language.__LANGUAGE_NAMES.keys()

    @staticmethod
    def get_all_languages():
        return Language.__LANGUAGE_NAMES.items()


class LanguageManager:
    _curr_lang = Language.PT

    @classmethod
    def get_language(cls):
        return cls._curr_lang

    @classmethod
    def set_language(cls, lang: str):
        cls._curr_lang = Language(lang)
