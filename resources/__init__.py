from itertools import product

from resources.drivers.database import database
from resources.config import config
import discord.ext.commands

from resources.top_gg import setup_top_gg


def get_command_prefix(_, __):
    prefix = config.BOT_PREFIX
    return set(
        [
            "".join(
                [
                    prefix[i].lower() if cases[i] else prefix[i].upper()
                    for i in range(len(cases))
                ]
            )
            for cases in product([True, False], repeat=len(prefix))
        ]
    )


bot = discord.ext.commands.Bot(
    command_prefix=get_command_prefix,
    help_command=None,
    case_insensitive=True,
    owner_id=330148908531580928,
)

from resources import commands
from resources.commands import calender_view
from resources.errors import errors_event
from resources.domain_logic import bot_tasks

setup_top_gg(bot)

database.load()
