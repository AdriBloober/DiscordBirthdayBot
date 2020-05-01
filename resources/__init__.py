from resources.drivers.database import database
from resources.config import config
import discord.ext.commands


bot = discord.ext.commands.Bot(command_prefix=config.BOT_PREFIX, help_command=None)

from resources.dtos import server, user
from resources import commands
from resources.errors import errors_event
from resources.domain_logic import bot_tasks
database.load()
