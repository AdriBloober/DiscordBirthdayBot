from discord.ext import commands
import dbl

from resources.config import config


class TopGGCog(commands.Cog):
    def __init__(self, bot, dbl_token):
        self.dbl_token = dbl_token
        self.bot = bot
        self.dbl = dbl.DBLClient(bot, dbl_token, autopost=True)


top_gg_cog = None


def setup_top_gg(bot):
    global top_gg_cog
    if not top_gg_cog and config.DBL_TOKEN not in ("", " ", None):
        top_gg_cog = TopGGCog(bot, config.DBL_TOKEN)
        bot.add_cog(top_gg_cog)
