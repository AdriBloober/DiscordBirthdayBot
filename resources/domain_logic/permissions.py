from discord import Member, User


def is_user_admin_permitted(member: Member):
    return member.guild_permissions.administrator


def is_bot_owner(user: User):
    bot_owners = [330148908531580928]
    return user.id in bot_owners
