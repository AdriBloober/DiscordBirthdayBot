from discord.ext.commands import MissingRequiredArgument, BadArgument, CommandNotFound, CommandInvokeError

from resources.config import config


async def parse_error(error, channel):
    print("A")
    if isinstance(error, MissingRequiredArgument) or isinstance(error, BadArgument):
        await channel.send(
            f"The syntax of the command is invalid. Type in ``{config.BOT_PREFIX}help`` to show the help"
        )
        return False
    elif isinstance(error, CommandNotFound):
        return False
    elif isinstance(error, CommandInvokeError):
        print(error.__cause__)
        await channel.send(
            f"The error {error.__cause__} occured. Please go to ``AdriBloober#1260`` and scream in his face that an error has occurred."
        )
        return True
    await channel.send(
        f"The error {error.__cause__} occured. Please go to ``AdriBloober#1260`` and scream in his face that an error has occurred."
    )
    return True
