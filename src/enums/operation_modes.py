from enum import Enum


class OperationMode(Enum):
    __DESPRIPTION_MODES = {
        "tts": "Text-to-Speech",
        "pb": "Playback",
    }

    TTS = "tts"
    PLAYBACK = "pb"

    @staticmethod
    def get_mode(mode: str):
        return OperationMode.__DESPRIPTION_MODES[mode]

    @staticmethod
    def get_available_modes():
        return [mode.value for mode in OperationMode]

    @staticmethod
    def get_all_modes():
        return OperationMode.__DESPRIPTION_MODES.items()
