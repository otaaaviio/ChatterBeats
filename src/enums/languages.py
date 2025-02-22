from enum import Enum


class Language(Enum):
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

    @staticmethod
    def get_language(lang: str):
        return Language.__LANGUAGE_NAMES[lang]

    @staticmethod
    def get_available_languages():
        return Language.__LANGUAGE_NAMES.keys()

    @staticmethod
    def get_all_languages():
        return Language.__LANGUAGE_NAMES.items()
