import asyncio
import logging

from enums.operation_modes import ModeManager, OperationMode
from tasks.playback import process_msc
from tasks.queues import message_queue, music_queue
from tasks.tts import process_tts


async def process_messages():
    while True:
        try:
            op_mode = ModeManager.get_mode()

            if op_mode == OperationMode.TTS:
                if not message_queue.empty():
                    msg = await message_queue.get()
                    await process_tts(msg)
            elif op_mode == OperationMode.PLAYBACK:
                if not music_queue.empty():
                    msc = await music_queue.get()
                    await process_msc(msc)
        except Exception as err:
            logging.error(err)
        finally:
            await asyncio.sleep(1)
