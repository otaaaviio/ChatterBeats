import re
from discord.ext import commands


def remove_brackets_and_content(text: str) -> str:
    if text is None:
        return ""
    return re.sub(r"\s*[\(\[].*?[\)\]]", "", text).strip()


class Music:
    def __init__(self, ydl_info, ctx=None):
        self.id = ydl_info.get("id", None)
        self.url = ydl_info.get("url", None)
        self.title = remove_brackets_and_content(ydl_info.get("title", None))
        self.playtime = ydl_info.get("duration_string", None)
        self.video_url = ydl_info.get("webpage_url", None)
        self.ctx: commands.Context = ctx
