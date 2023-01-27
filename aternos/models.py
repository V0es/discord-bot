from typing import Optional, List

import sqlalchemy as db

engine = db.create_engine('sqlite:///aternos/users.db')

connection = engine.connect()

metadata = db.MetaData()

users = db.Table('users', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('public_username', db.String(32), nullable=False),
    db.Column('aternos_username', db.String(32), nullable=False),
    db.Column('aternos_password', db.String(32), nullable=False))


metadata.create_all(engine)

def insert(values : Optional[List[str]]):
    vals_to_insert = []
    for user in values:
        vals_to_insert.append({
            'public_username' : user[0],
            'aternos_username' : user[1],
            'aternos_password' : user[2]
        })
    insertion_query = users.insert().values(values)
    connection.execute(insertion_query)


def select_all():
    select_all_query = db.select([users])
    result = connection.execute(select_all_query)

    return result.fetchall()