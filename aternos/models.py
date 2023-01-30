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


def get_rand_str(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))



engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


for i in range(10000):
    usr = User(get_rand_str(32), get_rand_str(32), get_rand_str(32))
    session.add(usr)
    session.commit()

result = session.query(User).all()
print(result)



