from discord.ext import commands

allowed_errors = [
        commands.MissingPermissions,
        commands.MissingRole,
        commands.MissingAnyRole,
        commands.MissingRequiredArgument,
        commands.BadArgument,
        commands.CommandNotFound,
        commands.BotMissingPermissions,
        commands.CommandOnCooldown
    ]