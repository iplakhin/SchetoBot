from datetime import datetime
from typing import NamedTuple

from db import db


class Report(NamedTuple):
    cash: int
    my: int
    to_return: int
    extra: int
    total_my: int
    withdrawal: int

def new_user(user_id: int):
    db.create_user(user_id=user_id)
    return


def add_income_or_withdraw(data: dict[str, str | int]):
    telegram_id = data.get('telegram_id', 0)
    title = data.get('title', 'error')
    amount = data.get('amount', db.get_price(title))
    tag = data.get('tag', 'error')
    try:
        answer = db.insert_income(telegram_id, title, amount, tag)
    except:
        raise ValueError('Ошибка записи в БД')
    if tag == 'cash':
        my_money = db.get_price(title)
        try:
            db.insert_income(telegram_id, title, amount=my_money, tag='my')
        except:
            raise ValueError('Ошибка записи в БД')
    if tag == 'withdraw':
        return f"Списано: {answer[1]} руб."
    else:
        return f"Добавлено:\n {answer[0]} {answer[1]} руб."


def show_budget(uid: int) -> Report:
    first_day_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    data = db.show_budget(first_day_month, uid)
    data = {key: value if value else 0 for key, value in data.items()}
    report = Report(
        cash=data.get('cash'),
        my=data.get('my'),
        to_return=data.get('cash') - data.get('my') if data.get('cash') > data.get('my') else 0,
        extra=data.get('extra'),
        withdrawal=data.get('withdrawal'),
        total_my=data.get('my') + data.get('extra')
    )
    return report


def new_price(data: dict[str, str | int]):
    title = data.get('title', 'error')
    price = data.get('price', 0)
    try:
        answer = db.set_new_price(title, price)
    except:
        raise ValueError('Ошибка записи в БД')
    return answer


def drop_base():
    db.drop_base()
    return "База очищена. Отправьте команду /start"