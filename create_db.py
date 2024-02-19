from environs import Env
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from models.models import Base, Price


def set_initial_prices():
    env = Env()
    env.read_env()
    title = list(env("TITLE").split(','))
    price = list(map(int, env("PRICE").split(',')))
    PRICES = [{'title': title[i], 'price': price[i]} for i in range(len(title))]

    with (session_factory() as session):
        session.execute(insert(Price).values(PRICES))
        session.commit()
    return


engine = create_engine("sqlite:///expenses.db")
session_factory = sessionmaker(engine)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

set_initial_prices()
