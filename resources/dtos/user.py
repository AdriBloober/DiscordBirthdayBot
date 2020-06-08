from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from resources.commands.converters import Birthday
from resources.drivers.database import database


class User(database.db):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(String(32), nullable=False)
    birthday = Column(String(5), nullable=False)
    last_birthday = Column(String(4), nullable=True)

    def __init__(self, user, birthday):
        self.user_id = user.id
        self.birthday = birthday


def initialize_user(user, birthday):
    user = User(user, birthday)
    database.session.add(user)
    database.session.commit()
    print(f"The user {user} has been initialized")
    return user


def get_user(user):
    return database.session.query(User).filter(User.user_id == user.id).one()


def remove_user(user):
    database.session.delete(user)
    database.session.commit()


def update_birthday(user, birthday):
    user.birthday = birthday
    database.session.commit()


def update_last_birthday(user, last_birthday):
    user.last_birthday = last_birthday
    database.session.commit()


def get_all_users_where_birthday(birthday):
    try:
        return database.session.query(User).filter(User.birthday == birthday).all()
    except NoResultFound:
        return []


def count_users() -> int:
    return database.session.query(User).count()


def get_all_users():
    try:
        return database.session.query(User).all()
    except NoResultFound:
        return []


def get_last_birthday(users):
    last_birthday: Birthday = None
    last_birthday_users = []
    now = datetime.now()
    for user in users:
        b = Birthday.from_string(user.birthday)
        if user.last_birthday == str(now.year) and b.to_date(now.year) < now:
            if last_birthday is None or last_birthday.to_date(now.year) < b.to_date(
                now.year
            ):
                last_birthday = b
                last_birthday_users.clear()
                last_birthday_users.append(user)
            elif last_birthday == b:
                last_birthday_users.append(user)
    return last_birthday, last_birthday_users


def get_next_birthday(users):
    next_birthday: Birthday = None
    next_birthday_users = []
    now = datetime.now()
    for user in users:
        b = Birthday.from_string(user.birthday)
        if (user.last_birthday is None or user.last_birthday != str(now.year)) and b.to_date(
            now.year
        ) > now:
            if next_birthday is None or next_birthday.to_date(now.year) > b.to_date(
                now.year
            ):
                next_birthday = b
                next_birthday_users.clear()
                next_birthday_users.append(user)
            elif next_birthday == b:
                next_birthday_users.append(user)
    return next_birthday, next_birthday_users
