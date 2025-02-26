import asyncio

music_queue = asyncio.Queue(maxsize=20)
message_queue = asyncio.Queue(maxsize=50)
