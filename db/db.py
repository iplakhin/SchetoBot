from sqlalchemy import create_engine, func, select, insert, and_, update
from sqlalchemy.orm import sessionmaker
from models.models import User, Income, Price

engine = create_engine('sqlite:///expenses.db')
session_factory = sessionmaker(engine)


def get_user(user_id: int):
    with session_factory() as session:
        user = session.execute(select(User).where(User.telegram_id == user_id)).one_or_none()
        return user


def create_user(user_id: int):
    with (session_factory() as session):
        is_admin = True if user_id in [361046129, 544312899] else False
        new_user = User(telegram_id=user_id, is_admin=is_admin)
        session.add(new_user)
        session.commit()
        return new_user


def insert_income(telegram_id: int, title: str, amount: int, tag: str):
    with session_factory() as session:
        upk = session.execute(select(User.pk).where(User.telegram_id == telegram_id)).one_or_none()
        session.execute(insert(Income).values(user_pk=upk[0],
                                              title=title,
                                              amount=amount,
                                              tag=tag))
        session.commit()
        return title, amount


def show_budget(first_day_month, uid: int) -> dict[
    str, int | None]:  # по месяцу select sum(amount) as total from expenses where (date BETWEEN date("2023-10-01") AND date("2023-10-31")) AND user_pk=(select pk from user WHERE telegram_id="544312899")
    with session_factory() as session:
        total_cash = session.execute(
            select(func.sum(Income.amount).label("cash")).filter(and_(
                Income.created_at >= first_day_month,
                Income.tag == 'cash',
                Income.user_pk == select(User.pk).filter_by(telegram_id=uid).scalar_subquery()
            )
            )).fetchone()
        my_cash = session.execute(
            select(func.sum(Income.amount).label("my")).filter(and_(
                Income.created_at >= first_day_month,
                Income.tag == 'my',
                Income.user_pk == select(User.pk).filter_by(telegram_id=uid).scalar_subquery()
            )
            )).fetchone()
        extra = session.execute(
            select(func.sum(Income.amount).label("extra")).filter(and_(
                Income.created_at >= first_day_month,
                Income.tag == 'extra',
                Income.user_pk == select(User.pk).filter_by(telegram_id=uid).scalar_subquery()
            )
            )).fetchone()
        withdrawal = session.execute(
            select(func.sum(Income.amount).label("withdrawal")).filter(and_(
                Income.created_at >= first_day_month,
                Income.tag == 'withdraw',
                Income.user_pk == select(User.pk).filter_by(telegram_id=uid).scalar_subquery()
            )
            )).fetchone()
        return {'cash': total_cash[0],
                'my': my_cash[0],
                'extra': extra[0],
                'withdrawal': withdrawal[0]}


def get_price(title: str):
    with session_factory() as session:
        price = session.execute(select(Price.price).filter_by(title=title)).one_or_none()
        if price:
            return price[0]
        return price


def set_new_price(title, price):
    with session_factory() as session:
        session.execute(update(Price).values(price=price).where(Price.title == title))
        session.commit()
    return f"{title}: {price}"


def drop_base():
    pass


def check_permission(user_id: int):
    with session_factory() as session:
        user: User = get_user(user_id)[0]
        if not user:
            return False
        if user.is_admin:
            return True
        return False
