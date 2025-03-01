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
                msg = await asyncio.wait_for(message_queue.get(), timeout=1)
                await process_tts(msg)
            elif op_mode == OperationMode.PLAYBACK:
                msc = await asyncio.wait_for(music_queue.get(), timeout=1)
                await process_msc(msc)
        except Exception as err:
            logging.error(err)
        except asyncio.TimeoutError:
            pass
        finally:
            await asyncio.sleep(0.2)
