from discord.ext import commands


class Music:
    def __init__(self, ydl_info, ctx=None):
        self.id = ydl_info.get("id", None)
        self.url = ydl_info.get("url", None)
        self.title = ydl_info.get("fulltitle", None)
        self.playtime = ydl_info.get("duration_string", None)
        self.video_url = ydl_info.get("webpage_url", None)
        self.ctx: commands.Context = ctx
