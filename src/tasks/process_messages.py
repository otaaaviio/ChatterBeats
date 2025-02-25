import asyncio
import logging

from enums.operation_modes import OperationMode
from tasks.playback import process_msc, music_queue
from tasks.tts import message_queue, process_tts


async def process_messages(bot):
    while True:
        try:
            general_commands = bot.get_cog("GeneralCommands")

            if general_commands is None:
                continue

            op_mode = general_commands.op_mode
            curr_lang = general_commands.curr_lang.value

            if op_mode == OperationMode.TTS:
                msg = await message_queue.get()
                if msg:
                    await process_tts(msg, curr_lang)
            elif op_mode == OperationMode.PLAYBACK:
                msc = await music_queue.get()
                if msc:
                    await process_msc(msc)
        except Exception as err:
            logging.error(err)
        finally:
            await asyncio.sleep(1)
