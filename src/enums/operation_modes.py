from enum import Enum


class OperationMode(Enum):
    TTS = "tts"
    PLAYBACK = "pb"

    __DESPRIPTION_MODES = {
        "tts": "Text-to-Speech",
        "pb": "Playback",
    }

    @staticmethod
    def get_description_mode(mode: str):
        return OperationMode.__DESPRIPTION_MODES[mode]

    @staticmethod
    def get_available_modes():
        return [mode.value for mode in OperationMode]

    @staticmethod
    def get_all_modes():
        return OperationMode.__DESPRIPTION_MODES.items()
    
class ModeManager():
    _op_mode = OperationMode.TTS
    
    @classmethod
    def get_mode(cls):
        return cls._op_mode
    
    @classmethod
    def set_mode(cls, mode: str):
        cls._op_mode = OperationMode(mode)
