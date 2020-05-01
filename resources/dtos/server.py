from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from resources.drivers.database import database


class Server(database.db):
    __tablename__ = "servers"
    id = Column(Integer, nullable=False, primary_key=True)
    guild_id = Column(String(32), nullable=False)
    notification_channel_id = Column(String(32), nullable=True)

    def __init__(self, guild):
        self.guild_id = guild.id


def initialize_server(guild):
    server = Server(guild)
    database.session.add(server)
    database.session.commit()
    print(f"The server {guild.name} has been initialized")
    return server


def get_server(guild):
    try:
        return database.session.query(Server).filter(Server.guild_id == guild.id).one()
    except NoResultFound:
        return initialize_server(guild)
    except MultipleResultsFound:
        remove_server(guild)
        initialize_server(guild)
        print(f"The server {guild.name} was reconfigured. All data was removed.")


def get_servers(guild):
    try:
        return database.session.query(Server).filter(Server.guild_id == guild.id).all()
    except NoResultFound:
        return []


def remove_server(guild):
    for server in get_servers(guild):
        database.session.delete(server)
    database.session.commit()


def update_notification_channel(server, channel):
    server.notification_channel_id = channel.id
    database.session.commit()
