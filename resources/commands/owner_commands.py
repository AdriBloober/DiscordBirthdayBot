import aiohttp
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands

from resources import bot
from resources.config import config
from resources.domain_logic.permissions import is_bot_owner
from resources.dtos.user import count_users


class OwnerCommands(commands.Cog):
    @commands.command()
    async def get_servers(self, ctx, *args):
        enable_joined_at = True
        if len(args) == 1 and args[0].lower() in ("false", "no"):
            enable_joined_at = False
        if not is_bot_owner(ctx.author):
            await ctx.send("You don't have the bot owner permission!")
            return
        guilds = []
        for g in bot.guilds:
            s = f"{g.name} -> {g.owner}"
            if enable_joined_at:
                s += f" -> {g.get_member(bot.user.id).joined_at.isocalendar()}"
            guilds.append(s)
        guilds.append("---")
        guilds.append(f"Users: {count_users()}")


        msgs = [[]]
        for g in guilds:
            if len(msgs[len(msgs) - 1]) > 35:
                msgs.append([])
            msgs[len(msgs) - 1].append(g)
        for msg in msgs:
            await ctx.send("```" + "\n".join(msg) + "```")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if config.ADMIN_WEBHOOK_URL not in ["", " ", None]:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    config.ADMIN_WEBHOOK_URL, adapter=AsyncWebhookAdapter(session)
                )
                await webhook.send(
                    f"The server {guild.name} by {guild.owner} is now using this bot. {len(bot.guilds)} guilds are using the bot.",
                    username="DiscordBirthdayBot",
                )
