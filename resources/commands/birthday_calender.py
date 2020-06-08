from datetime import datetime

from discord.ext import commands

from resources import bot
from resources.commands.converters import Birthday
from resources.dtos.user import (
    get_all_users_where_birthday,
    get_next_birthday,
    get_last_birthday, get_all_users,
)


def parse_global(args):
    if len(args) > 0 and args[0].lower() in ("g", "global", "yes"):
        return True
    return False


class BirthdayCalendar(commands.Cog):
    @commands.command()
    async def who_has_today_birthday(self, ctx, *args):
        g = parse_global(args)
        users = get_all_users_where_birthday(
            Birthday.from_datetime(datetime.now()).__str__()
        )
        if g and len(users) > 10:
            await ctx.send(
                "More then 10 global users have today birthday. Global is disabled!"
            )
            g = False
        if not g:
            new_users = []
            for user in users:
                if ctx.guild.get_member(int(user.user_id)) is not None:
                    new_users.append(user)
            users = new_users
        if len(users) == 0:
            await ctx.send("Nobody has birthday today.")
        else:
            await ctx.send(
                "All this/these user(s) have today birthday: "
                + ", ".join([f"``{bot.get_user(int(user.user_id)).name}``" for user in users])
                + "."
            )

    @commands.command()
    async def who_has_next_birthday(self, ctx):
        users = get_all_users()
        new_users = []
        for user in users:
            if ctx.guild.get_member(int(user.user_id)) is not None:
                new_users.append(user)

        birthday, users = get_next_birthday(new_users)

        if len(users) == 0:

            await ctx.send("Nobody has a birthday this year.")
        else:
            await ctx.send(
                f"At the day {birthday} this/these user(s) have next birthday: "
                + ", ".join([f"``{bot.get_user(int(user.user_id)).name}``" for user in users])
                + "."
            )

    @commands.command()
    async def who_has_last_birthday(self, ctx):
        users = get_all_users()
        new_users = []
        for user in users:
            if ctx.guild.get_member(int(user.user_id)) is not None:
                new_users.append(user)
        birthday, users = get_last_birthday(new_users)

        if len(users) == 0:

            await ctx.send("No one has had a birthday this year.")
        else:
            await ctx.send(
                f"At the day {birthday} this/these user(s) have last birthday: "
                + ", ".join([f"``{bot.get_user(int(user.user_id)).name}``" for user in users])
                + "."
            )
