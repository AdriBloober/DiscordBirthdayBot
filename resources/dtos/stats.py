from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from resources import bot
from resources.commands.converters import Birthday
from resources.drivers.database import database
from resources.dtos.server import Server
from resources.dtos.user import User


class Stats(database.db):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    guilds = Column(Integer, nullable=False)
    configured_guilds = Column(Integer, nullable=False)
    users = Column(Integer, nullable=False)
    users_with_birthday = Column(Integer, nullable=False)
    users_with_past_birthday = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(
        self,
        guilds,
        configured_guilds,
        users,
        users_with_birthday,
        users_with_past_birthday,
    ):
        assert configured_guilds <= guilds
        self.guilds = guilds
        self.configured_guilds = configured_guilds
        self.users = users
        self.users_with_birthday = users_with_birthday
        self.users_with_past_birthday = users_with_past_birthday
        self.timestamp = datetime.now()


def create_stat():
    guilds = len(bot.guilds)
    configured_guilds = database.session.query(Server).count()
    users = 0
    for g in bot.guilds:
        users += g.member_count
    users_with_birthday = database.session.query(User).count()
    users_with_past_birthday = (
        database.session.query(User)
        .filter(User.last_birthday == str(Birthday.from_datetime(datetime.now())))
        .count()
    )
    database.session.add(
        Stats(
            guilds,
            configured_guilds,
            users,
            users_with_birthday,
            users_with_past_birthday,
        )
    )
    database.session.commit()
