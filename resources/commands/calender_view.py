from datetime import datetime
from typing import List

from discord import Guild, Message, Embed, Member, Reaction, Forbidden

from resources import bot
from resources.commands.converters import Birthday
from resources.dtos.user import get_all_users_where_birthday, User


def is_int_parsable(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def generate_embed(guild, month):
    embed1 = Embed(title=f"Calender view for month {month}. 1/2")
    embed2 = Embed(title=f"Calender view for month {month}. 2/2")
    for d in range(1, 31):
        users = get_all_users_where_birthday(Birthday(d, month).__str__())
        new_users = []
        for user in users:
            if guild.get_member(int(user.user_id)) is not None:
                new_users.append(user)
        v = ", ".join([bot.get_user(int(user.user_id)).mention for user in new_users])
        if v == "":
            v = "-"
        if d < 16:
            embed1.add_field(name=str(d), value=v, inline=True)
        else:
            embed2.add_field(name=str(d), value=v, inline=True)
    return embed1, embed2


class CalenderView:
    def __init__(self, guild: Guild, message: Message, first_message: Message, orginal_message, author: Member, month: int):
        self.guild = guild
        self.message = message
        self.second_message = first_message
        self.orginal_message = orginal_message
        self.author = author
        self.month = month

    async def regenerate_embed(self):
        e1, e2 = generate_embed(self.guild, self.month)
        await self.second_message.edit(embed=e1)
        await self.message.edit(embed=e2)


calender_views: List[CalenderView] = []


@bot.command(aliases=["c", "view_calender", "birthdays"])
async def calender(ctx, *args):
    if len(args) > 0 and is_int_parsable(args[0]):
        month = int(args[0])
    else:
        month = datetime.now().month

    e1, e2 = generate_embed(ctx.guild, month)
    first_message = await ctx.send(embed=e1)
    message = await ctx.send(embed=e2)
    await message.add_reaction("◀️")
    await message.add_reaction(b"\xf0\x9f\x97\x91\xef\xb8\x8f".decode())
    await message.add_reaction("▶️")

    view = CalenderView(ctx.guild, message, first_message, ctx.message, ctx.message.author, month)
    calender_views.append(view)


@bot.event
async def on_reaction_add(reaction: Reaction, user: User):
    if user.id == bot.user.id:
        return
    for view in calender_views:
        if reaction.message.id == view.message.id:
            if reaction.emoji.encode() == b'\xe2\x97\x80\xef\xb8\x8f':
                view.month -= 1
                if view.month < 1:
                    view.month = 12
                await reaction.remove(user)
                await view.regenerate_embed()
            elif reaction.emoji.encode() == b'\xe2\x96\xb6\xef\xb8\x8f':
                view.month += 1
                if view.month > 12:
                    view.month = 1
                await reaction.remove(user)
                await view.regenerate_embed()
            elif reaction.emoji.encode() == b"\xf0\x9f\x97\x91\xef\xb8\x8f":
                if user.id == view.author.id:
                    await view.message.delete()
                    await view.second_message.delete()
                    try:
                        await view.orginal_message.delete()
                    except Forbidden:
                        await reaction.message.channel.send("I don't have permissions to delete a message :c")
                else:
                    await reaction.remove(user)
