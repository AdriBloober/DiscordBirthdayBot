from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm.exc import NoResultFound

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
