import discord
from discord import TextChannel, Member, User
from discord.ext.commands import BadArgument
from sqlalchemy.orm.exc import NoResultFound

from resources import bot
from resources.commands.birthday_calender import BirthdayCalendar
from resources.commands.converters import BirthdayConverter
from resources.commands.owner_commands import OwnerCommands
from resources.config import config
from resources.domain_logic.permissions import is_bot_owner, is_user_admin_permitted
from resources.dtos.user import (
    get_user,
    initialize_user,
    update_birthday,
    remove_user,
)
from resources.dtos.server import get_server, update_notification_channel


@bot.command()
async def help(ctx):
    helps = []
    helps.append(f"{config.BOT_PREFIX}help : Shows this help.")
    helps.append(f"{config.BOT_PREFIX}set_birthday  Day-Month : Set your birthday.")
    helps.append(f"{config.BOT_PREFIX}birthday : Shows your birthday.")
    helps.append(f"{config.BOT_PREFIX}birthday @he : Shows hist birthday.")
    helps.append(f"{config.BOT_PREFIX}birthday delete : Forget your birthday.")
    helps.append(
        f"{config.BOT_PREFIX}today [global] : Shows users, that have today birthday. If you "
        f"add 'global' after the command, you will see global birthdays for today."
    )
    helps.append(f"{config.BOT_PREFIX}last : Shows the last birthday on the server.")
    helps.append(f"{config.BOT_PREFIX}next : Shows the next birthday on the server.")
    helps.append(
        f"{config.BOT_PREFIX}birthdays [Month] : Shows a calender of birthdays. If the month is not set, i will use "
        f"the current month. "
    )
    if is_user_admin_permitted(ctx.author):
        helps.append(
            f"{config.BOT_PREFIX}set_notification_channel '#channel' : Set the notification channel. The bot "
            f"sends bithday notifications in this channel"
        )
    helps.append("Information")
    helps.append(f"{config.BOT_PREFIX}invite : Invite this bot to your server.")
    helps.append(f"{config.BOT_PREFIX}github : Get the github link.")
    helps.append("A [argument] means, that the argument is optional.")
    helps.append("Developed by AdriBloober#1260 (https://adribloober.wtf)")
    helps.append("AdriBloober's Twitter: https://twitter.com/AdriBloober")
    message = "```"
    for i in helps:
        message += i + "\n"
    message += "```"
    await ctx.send(message)


@bot.command()
async def invite(ctx):
    try:
        await ctx.author.send("Invite link: " + config.INVITE_LINK)
        await ctx.message.add_reaction("✅")
    except discord.Forbidden:
        await ctx.send(
            "I cannot send you a direct message. Please enable direct messaging!"
        )


@bot.command()
async def github(ctx):
    await ctx.send(config.GITHUB_LINK)


@bot.command(aliases=["my_birthday_is"])
async def set_birthday(ctx, birthday: BirthdayConverter):
    try:
        update_birthday(get_user(ctx.author), str(birthday))
        await ctx.send(
            f"I have set your birthday to {birthday}! Your birthday will be shown publicly. Delete your birthday with ``{config.BOT_PREFIX}birthday delete``."
        )
    except NoResultFound:
        initialize_user(ctx.author, str(birthday))
        await ctx.send(
            f"Hello, i see you are new! I have set your birthday to {birthday}! Your birthday will be shown publicly. Delete your "
            f"birthday with ``{config.BOT_PREFIX}forget_my_birthday``. "
        )


@bot.command(aliases=["when_is_my_birthday", "when_is_his_birthday"])
async def birthday(ctx, *args):
    target_user = ctx.author
    if len(args) == 1 and args[0].lower() in ("del", "delete", "remove", "forget"):
        try:
            user = get_user(ctx.author)
            remove_user(user)
            await ctx.send("Ok i dont know who you are!")
        except NoResultFound:
            await ctx.send(f"I didnt know your birthday.")
        return
    elif len(args) == 1:
        try:
            target_user_id = int(
                args[0]
                .replace("<", "")
                .replace(">", "")
                .replace("@", "")
                .replace("!", "")
            )
            target_user = bot.get_user(target_user_id)
        except ValueError:
            raise BadArgument("Target user")
    elif len(args) > 1:
        raise BadArgument("Target user")
    try:
        user = get_user(target_user)
        if user.birthday is not None:
            await ctx.send(f"Your birthday is {user.birthday} ^^")
        else:
            await ctx.send(f"I dont know")
    except NoResultFound:
        await ctx.send(f"I dont know")


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
async def forget_his_birthday(ctx, member: Member):
    if not is_bot_owner(ctx.author):
        await ctx.send(
            "NOOO, you can delete your own birthday, but not the birthday of others!"
        )
        return
    try:
        user = get_user(member)
        remove_user(user)
        await ctx.send("Ok i dont know who he are!")
    except NoResultFound:
        await ctx.send(f"I didnt know his birthday.")


bot.add_cog(OwnerCommands())
bot.add_cog(BirthdayCalendar())
