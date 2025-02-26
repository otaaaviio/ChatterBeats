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
                try:
                    msg = await asyncio.wait_for(message_queue.get(), timeout=1)
                    await process_tts(msg)
                except asyncio.TimeoutError:
                    pass
            elif op_mode == OperationMode.PLAYBACK:
                try:
                    msc = await asyncio.wait_for(music_queue.get(), timeout=1)
                    await process_msc(msc)
                except asyncio.TimeoutError:
                    pass
        except Exception as err:
            logging.error(err)
        finally:
            await asyncio.sleep(1)
