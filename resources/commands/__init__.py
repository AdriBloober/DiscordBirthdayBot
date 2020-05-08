from discord import TextChannel, Member
from sqlalchemy.orm.exc import NoResultFound

from resources import bot
from resources.commands.converters import BirthdayConverter
from resources.config import config
from resources.domain_logic.permissions import is_bot_owner, is_user_admin_permitted
from resources.dtos.user import (
    get_user,
    initialize_user,
    update_birthday,
    User,
    remove_user,
)
from resources.dtos.server import get_server, update_notification_channel


@bot.command()
async def help(ctx):
    helps = []
    helps.append(f"{config.BOT_PREFIX}help : Shows this help")
    helps.append(f"{config.BOT_PREFIX}my_birthday_is 'Day-Month' : Set your birthday")
    helps.append(f"{config.BOT_PREFIX}when_is_my_birthday : Shows your birthday")
    helps.append(f"{config.BOT_PREFIX}when_is_his_birthday <@he> : Shows hist birthday")
    helps.append(f"{config.BOT_PREFIX}forget_my_birthday : Shows hist birthday")
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
async def his_birthday_is(ctx, member: Member, birthday: BirthdayConverter):
    if not is_bot_owner(ctx.author):
        await ctx.send(
            "NOOO, you can set your own birthday, but not the birthday of others!"
        )
        return
    try:
        update_birthday(get_user(member), str(birthday))
        await ctx.send("I have set his birthday :D")
    except NoResultFound:
        initialize_user(member, str(birthday))
        await ctx.send("Hello, i see he is new here! I have set his birthday ^^")


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
        await ctx.send(
            f"I have no permissions to write in the channel {channel.mention} :c"
        )
        return
    update_notification_channel(get_server(ctx.guild), channel)
    await ctx.send("I have set the new notification channel.")


@bot.command()
async def when_is_my_birthday(ctx):
    try:
        user = get_user(ctx.author)
        if user.birthday is not None:
            await ctx.send(f"Your birthday is {user.birthday} ^^")
        else:
            await ctx.send(f"I dont know")
    except NoResultFound:
        await ctx.send(f"I dont know")


@bot.command()
async def when_is_his_birthday(ctx, member: Member):
    try:
        user = get_user(member)
        if user.birthday is not None:
            await ctx.send(f"His birthday is {user.birthday} ^^")
        else:
            await ctx.send(f"I dont know")
    except NoResultFound:
        await ctx.send(f"I dont know")


@bot.command()
async def forget_my_birthday(ctx):
    try:
        user = get_user(ctx.author)
        remove_user(user)
        await ctx.send("Ok i dont know who you are!")
    except NoResultFound:
        await ctx.send(f"I didnt know your birthday.")


@bot.command()
async def forget_his_birthday(ctx, member: Member):
    if not is_bot_owner(ctx.author):
        await ctx.send(
            "NOOO, you can delete your own birthday, but not the birthday of others!"
        )
        return
    try:
        user = get_user(member)
        remove_user(user)
        await ctx.send("Ok i dont know who you are!")
    except NoResultFound:
        await ctx.send(f"I didnt know your birthday.")
