import pickle
from datetime import datetime
from typing import NamedTuple

from db import db


class Expense(NamedTuple):
    title: str
    amount: int


def set_flags(withdraw_fl=False, price_fl=False, btn_name=None):
    flags = {'withdraw_fl': withdraw_fl, 'price_fl': price_fl, 'btn_name': btn_name}
    with open('flags.pkl', 'wb') as file:
        pickle.dump(flags, file)


def new_user(user_id: int):
    db.new_user(user_id=user_id)
    return


def add_expense(uid: int, message: str):  # message = Название кнопки
    title = message
    amount = db.get_price(message)
    expense = Expense(title=title,
                      amount=amount)
    if amount is None:
        return "Не понимаю. Выберите необходимую команду"
    answer = db.insert_expense(uid, expense)
    if answer:
        return f"Добавлено:\n{answer.title} {answer.amount}"
    else:
        raise Exception('Ошибка записи в БД')


def show_budget(uid: int):
    first_day_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    total = db.show_budget(first_day_month, uid)
    return f"За этот месяц вы заработали {total} руб."


def withdraw(uid: int, message: str):
    amount = -int(message)
    expense = Expense(title='Списание',
                      amount=amount)
    db.insert_expense(uid, expense)
    set_flags()
    return f"Списано: {expense.amount} руб"


def new_price(message: str):
    with open('flags.pkl', 'rb') as file:
        flags = pickle.load(file)
    title = flags['btn_name']
    price = int(message)
    answer = db.set_new_price(title, price)
    set_flags()
    return "Назначена новая цена: " + answer


def cancel(uid: int):
    return "Еще в разработке"


def check_flag(uid: int, message: str):
    with open('flags.pkl', 'rb') as file:
        flags = pickle.load(file)
    if flags['withdraw_fl'] is True:
        return withdraw(uid, message)
    elif flags['price_fl'] is True:
        return True
    elif flags['price_fl'] is False:
        return add_expense(uid, message)
