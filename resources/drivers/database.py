from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from resources.config import config


class Database:
    engine = None
    Session = None

    def __init__(self, host, port, user, password, db):
        self.db = declarative_base()
        self.database_uri = (
            f"mysql+pymysql://{user}:{password}@{host}:{str(port)}/{db}?charset=utf8"
        )
        self.engine = create_engine(self.database_uri)
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = self.session_maker(expire_on_commit=False)
        print("The database-ini was successful!")

    def load(self):
        self.db.metadata.create_all(self.engine)


database = Database(
    config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWORD, config.DB_DB
)
