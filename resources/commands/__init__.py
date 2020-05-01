from discord import TextChannel
from sqlalchemy.orm.exc import NoResultFound

from resources import bot
from resources.commands.converters import BirthdayConverter
from resources.config import config
from resources.domain_logic.permissions import is_user_admin_permitted
from resources.dtos.user import get_user, initialize_user, update_birthday
from resources.dtos.server import get_server, update_notification_channel


@bot.command()
async def help(ctx):
    helps = []
    helps.append(f"{config.BOT_PREFIX}help : Shows this help")
    helps.append(f"{config.BOT_PREFIX}my_birthday_is 'Day-Month' : Set your birthday")
    if is_user_admin_permitted(ctx.author):
        helps.append(
            f"{config.BOT_PREFIX}set_notification_channel '#channel' : Set the notification channel. The bot "
            f"sends bithday notifications in this channel"
        )
    helps.append("Developed by AdriBloober#1260")
    helps.append("AdriBloober's Twitter: https://twitter.com/AdriBloober")
    message = "```"
    for i in helps:
        message += i + "\n"
    message += "```"
    await ctx.send(message)


@bot.command()
async def my_birthday_is(ctx, birthday: BirthdayConverter):
    try:
        update_birthday(get_user(ctx.author), str(birthday))
        await ctx.send("I have set your birthday :D")
    except NoResultFound:
        initialize_user(ctx.author, str(birthday))
        await ctx.send("Hello, i see you are new! I have set your birthday ^^")


@bot.command()
async def set_notification_channel(ctx, channel: TextChannel):
    if not is_user_admin_permitted(ctx.author):
        await ctx.send("You don't have the administrator permission!")
        return
    if not ctx.author.permissions_in(channel):
        await ctx.send(
            f"You don't have permissions to write in the channel {channel.mention}!"
        )
        return
    member = ctx.guild.get_member(bot.user.id)
    if not member.permissions_in(channel):
        await ctx.send(f"I have no permissions to write in the channel {channel.mention} :c")
        return
    update_notification_channel(get_server(ctx.guild), channel)
    await ctx.send("I have set the new notification channel.")