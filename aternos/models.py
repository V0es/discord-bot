from datetime import datetime

import hashlib

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine, Integer, DateTime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    public_username: Mapped[str] = mapped_column(nullable=False)
    aternos_username: Mapped[str] = mapped_column(nullable=False)
    aternos_password: Mapped[str] = mapped_column(nullable=False)
    
    def __init__(self, public_username, aternos_username, aternos_password) -> None:
        self.timestamp = datetime.now()
        self.public_username = public_username
        self.aternos_username = aternos_username
        self.aternos_password = self.__md5encode(aternos_password)
        
    def __repr__(self) -> str:
        return f'id: {self.id}; time: {self.timestamp}, pub_us: {self.public_username}, \
            at_us: {self.aternos_username}, at_ps: {self.aternos_password}'

    @staticmethod
    def __md5encode(pwd: str) -> str:
        encoded = hashlib.md5(pwd.encode('utf-8'))
        return encoded.hexdigest().lower()


class Database():

    def __init__(self, db_path=None):
        if not db_path:
            db_path = ':memory:'
        
        self.engine = create_engine(f'sqlite:///{db_path}', echo=True)
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def get_all_users(self):
        result = self.session.query(User).all()
        print(type(result))
        return result

    def get_user_by_name(self, name: str):
        result = self.session.query(User).filter(User.public_username == name).all()
        print(type(result))
        return result

    def delete_all(self):
        self.session.query(User).filter(User.id >= 1).delete()
        self.session.commit()
