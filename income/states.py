from typing import NamedTuple
from aiogram.fsm.state import default_state, State, StatesGroup


class FSMSettings(StatesGroup):
    settings = State()
    input_value = State()


class FSMInputIncome(StatesGroup):
    qr_or_cash = State()
    input_amount = State()


class FSMWithdraw(StatesGroup):
    input_withdraw_amount = State()