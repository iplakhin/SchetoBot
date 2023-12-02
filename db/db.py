from sqlalchemy import create_engine, func, select, insert, and_, update
from sqlalchemy.orm import sessionmaker
from models.models import User, Expense, Prices

engine = create_engine('sqlite:///expenses.db')
session_factory = sessionmaker(engine)


def new_user(user_id: int):
    with (session_factory() as session):
        existed_user = session.execute(select(User).where(User.telegram_id == user_id)).one_or_none()
        if existed_user is None:
            is_admin = True if user_id in [361046129, 544312899] else False
            new_user = User(telegram_id=user_id, is_admin=is_admin)
            session.add(new_user)
            session.commit()
            return new_user
        else:
            return existed_user


def insert_expense(uid: int, expense):
    with session_factory() as session:
        u = session.execute(select(User.pk).where(User.telegram_id == uid)).one_or_none()
        session.execute(insert(Expense).values(user_pk=u[0],
                                               title=expense.title,
                                               amount=expense.amount))
        session.commit()
        return expense


def show_budget(first_day_month, uid: int) -> int:  # по месяцу select sum(amount) as total from expenses where (date BETWEEN date("2023-10-01") AND date("2023-10-31")) AND user_pk=(select pk from user WHERE telegram_id="544312899")
    with session_factory() as session:
        amount = session.execute(
            select(func.sum(Expense.amount).label("total")).filter(and_(
                Expense.created_at >= first_day_month,
                Expense.user_pk==select(User.pk).filter_by(telegram_id=uid)
            )
            )).fetchone()
        return amount[0]

def get_price(title: str):
    with session_factory() as session:
        price = session.execute(select(Prices.price).filter_by(title=title)).one_or_none()
        if price:
            return price[0]
        return price

def set_new_price(title, price):
    with session_factory() as session:
        session.execute(update(Prices).values(price=price).where(Prices.title == title))
        session.commit()
    return f"{title}: {price}"
