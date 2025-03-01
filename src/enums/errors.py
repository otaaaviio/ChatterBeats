from discord.ext import commands


class Error:
    __ALLOWED_ERRORS = [
        commands.MissingPermissions,
        commands.MissingRole,
        commands.MissingAnyRole,
        commands.MissingRequiredArgument,
        commands.BadArgument,
        commands.CommandNotFound,
        commands.BotMissingPermissions,
        commands.CommandOnCooldown,
    ]

    @staticmethod
    def get_allowed_errors():
        return Error.__ALLOWED_ERRORS
