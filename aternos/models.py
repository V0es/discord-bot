from typing import Optional, List

from datetime import datetime

import random, string

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine, String, Integer, DateTime, Text

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
        self.aternos_password = aternos_password
        
        
    
    def __repr__(self) -> str:
        return f'id: {self.id}; time: {self.timestamp}, pub_us: {self.public_username}, at_us: {self.aternos_username}, at_ps: {self.aternos_password}'


class Database():

    def __init__(self, db_path=None):
        if not db_path:
            db_path = ':memory:'
        
        self.engine = create_engine(f'sqlite:///{db_path}', echo=True)
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def add_user(self, user : User) -> None:
        self.session.add(user)
        self.session.commit()


    def get_all_users(self):
        result = self.session.query(User).all()
        print(type(result))
        return result

    def get_user_by_name(self, name : str):
        result = self.session.query(User).filter(User.public_username == name).all()
        print(type(result))
        return result


    def delete_all(self):
        self.session.query(User).filter(User.id >= 1).delete()
        self.session.commit()

def get_rand_str(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))




db = Database(db_path='aternos/users.db')

for i in range(50):

    usr = User(get_rand_str(32), get_rand_str(32), get_rand_str(32))
    db.add_user(usr)

db.add_user(User('smik', 'smiksss', '12345'))
print(db.get_all_users())
print(db.get_user_by_name('smik')[0].aternos_password)


db.delete_all()



