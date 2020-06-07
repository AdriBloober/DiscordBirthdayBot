import traceback

from resources import bot
from resources.errors.error_parser import parse_error


@bot.event
async def on_command_error(ctx, exception):
    if await parse_error(exception, ctx.channel):
        raise exception
