from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from config.config import load_config
from lexicon.lexicon import LEXICON_RU
from services import expenses
from keyboard import keyboard

router: Router = Router()

conf = load_config()


def auth(func):
    async def wrapper(message: Message):
        if message.from_user.id not in conf.tgbot.admin_id:
            return await message.answer("Вам запрещен доступ")
        return await func(message)

    return wrapper


@router.message(CommandStart())
@auth
async def start_bot(msg: Message):
    expenses.new_user(msg.from_user.id)
    expenses.set_flags()
    await msg.answer(text="Выберите необходимое действие",
                     reply_markup=keyboard.keyboard)


@router.message(F.text == "Списать")
@auth
async def withdraw(msg: Message):
    expenses.set_flags(True, False)
    await msg.answer(text="Введите сумму списания")


@router.message(F.text.in_(['Заказ гор', 'Забор гор', 'Заказ обл',
                            'Забор обл', 'Ложн гор', 'Ложн обл', 'Дист наст']))
@auth
async def add_expense(msg: Message):
    answer = expenses.check_flag(uid=msg.from_user.id, message=msg.text)
    if answer is True:
        expenses.set_flags(False, True, btn_name=msg.text)
        await msg.answer(text="Введите новую цену:")
    else:
        await msg.answer(text=answer)


@router.message(Command(commands=["settings"]))
@auth
async def settings(msg: Message):
    expenses.set_flags(False, True)
    await msg.answer(text="Выберите какую цену вы хотите изменить",
                     reply_markup=keyboard.keyboard)


@router.message(F.text.regexp(r'[\d{2, 4}]'))
@auth
async def get_number(msg: Message):
    answer = expenses.check_flag(uid=msg.from_user.id, message=msg.text)
    if answer is True:
        answer = expenses.new_price(msg.text)
        await msg.answer(text=answer, reply_markup=keyboard.keyboard)
    else:
        await msg.answer(text=answer, reply_markup=keyboard.keyboard)


@router.message(Command(commands=["account"]))
@auth
async def account_balance(msg: Message):
    answer = expenses.show_budget(msg.from_user.id)
    await msg.answer(text=answer, reply_markup=keyboard.keyboard)


@router.message(Command(commands=["help"]))
@auth
async def help(msg: Message):
    await msg.answer(text=LEXICON_RU["help_txt"])


@router.message(Command(commands=["cancel"]))
@auth
async def cancel(msg: Message):
    answer = expenses.cancel(msg.from_user.id)
    await msg.answer(text=answer, reply_markup=keyboard.keyboard)


@router.message()
@auth
async def other(msg: Message):
    await msg.answer(text="К сожалению, не понимаю, что вы хотите сказать. "
                          "Мой функционал ограничен. Для справки по командам отправьте /help ")
