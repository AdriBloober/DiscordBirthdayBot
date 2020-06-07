import asyncio
from datetime import datetime

import discord
from discord import Guild, Message, Forbidden

from resources import bot
from resources.config import config
from resources.commands.converters import Birthday
from resources.dtos.user import get_all_users_where_birthday, update_last_birthday, User, count_users
from resources.dtos.server import get_server, initialize_server, remove_server


async def server_status_update_task():
    while True:
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name=f"Active on {str(len(bot.guilds))} servers with {count_users()} users."),
        )
        await asyncio.sleep(60 * 5)  # wait 5 Minutes


async def birthday_task():
    while True:
        year = datetime.now().year
        users = get_all_users_where_birthday(
            str(Birthday.from_datetime(datetime.now()))
        )
        print(f"[NEW] loop with year {year} and available users length {len(users)}")
        for user in users:
            if user.last_birthday is None or int(user.last_birthday) < year:
                for guild in bot.guilds:
                    member = guild.get_member(int(user.user_id))
                    if not member is None:
                        server = get_server(guild)
                        if not server.notification_channel_id is None:
                            print(f"{member} birthday")
                            try:
                                await bot.get_channel(
                                    int(server.notification_channel_id)
                                ).send(
                                    f"{member.mention}: Today is your birthday! Happy Birthday from me ^^"
                                )
                                update_last_birthday(user, str(year))
                            except Forbidden:
                                owner: discord.User = guild.owner
                                dm = await owner.create_dm()
                                await dm.send(
                                    "Hello, i have no rights to write in any channel. So i will tell it you here: "
                                    + "I have no permissions to write in the notification channel. Please fix it!"
                                )

        await asyncio.sleep(60 * 60 * 4)


@bot.event
async def on_ready():
    bot.loop.create_task(server_status_update_task())
    bot.loop.create_task(birthday_task())
    print("Beeeeeeeep... boooting was succcessfullllyy... you can use me now [OOOOKKK]")


@bot.event
async def on_guild_join(guild: Guild):
    message = f"Welcome and thank you for the invite. With {config.BOT_PREFIX}help i will show you the help. You can set the birthday notification channel with {config.BOT_PREFIX}set_notification_channel #channel."
    get_server(guild)
    channel = None
    member = guild.get_member(bot.user.id)
    for i in guild.text_channels:
        if member.permissions_in(i):
            channel = i
            break

    if channel is None:
        owner: discord.User = guild.owner
        dm = await owner.create_dm()
        await dm.send(
            "Hello, i have no rights to write in any channel. So i will tell it you here: "
            + message
        )
    else:
        await channel.send(
            "I dont know, what channel i should use. Sorry, i hope this is the right channel. Here you have my default welcome text (sorry my creativity is limited): "
            + message
        )


@bot.event
async def on_guild_remove(guild: Guild):
    remove_server(guild)
    message = (
        "Why does you kick/ban meee :c Please tell us your opinion and your feedback."
    )
    dm = await guild.owner.create_dm()
    await dm.send(message)


@bot.event
async def on_message(message: Message):
    if bot.user.id != message.author.id and (
        message.content.startswith(bot.user.mention)
        or message.content.startswith(f"<@!{bot.user.id}>")
    ):
        await message.channel.send(
            f"Ehhhmm... you can use commands with my prefix: {config.BOT_PREFIX}. For example {config.BOT_PREFIX}help"
        )
    else:
        await bot.process_commands(message)
