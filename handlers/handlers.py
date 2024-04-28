from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from config.config import load_config
from lexicon.lexicon import LEXICON_RU, ERROR_MSG
from income import income
from income.states import FSMSettings, FSMWithdraw, FSMInputIncome
from keyboard import keyboard

router: Router = Router()

conf = load_config()


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(msg: Message):
    await msg.answer(text=LEXICON_RU['start_text'],
                     reply_markup=keyboard.keyboard)


        #################### Списание произвольной суммы #####################

@router.message(F.text == "Списать", StateFilter(default_state))
async def withdraw(msg: Message, state: FSMContext):
    await msg.answer(text="Введите сумму списания")
    await state.set_state(FSMWithdraw.input_withdraw_amount)
    await state.update_data(telegram_id=msg.from_user.id, title='Списание', tag='withdraw')


@router.message(StateFilter(FSMWithdraw.input_withdraw_amount), F.text.regexp(r'[\d{2, 6}]'))
async def withdraw_amount(msg: Message, state: FSMContext):
    await state.update_data(amount=-int(msg.text))
    answer = income.add_income_or_withdraw(await state.get_data())
    await msg.answer(text=answer, reply_markup=keyboard.keyboard)
    await state.clear()


@router.message(StateFilter(FSMWithdraw.input_withdraw_amount))
async def withdraw_amount(msg: Message):
    await msg.answer(text=ERROR_MSG['input_amount'])

# -----------------------------------------------------------------------

        ##################### Настройка кнопок ######################

@router.message(Command(commands=["settings"]), StateFilter(default_state))
async def settings(msg: Message, state: FSMContext):
    await msg.answer(text="Выберите какую цену вы хотите изменить",
                     reply_markup=keyboard.keyboard)
    await state.set_state(FSMSettings.settings)


@router.message(StateFilter(FSMSettings.settings),
                F.text.in_(['Заказ гор', 'Забор гор', 'Заказ обл',
                            'Забор обл', 'Ложн гор', 'Ложн обл',
                            'Миостим гор', 'Миостим обл', 'Дист наст']))
async def choose_button(msg: Message, state: FSMContext):
    await msg.answer(text="Введите новую цену:")
    await state.set_state(FSMSettings.input_value)
    await state.update_data(title=msg.text)


@router.message(StateFilter(FSMSettings.input_value), F.text.regexp(r'[\d{3, 5}]'))
async def set_new_price(msg: Message, state: FSMContext):
    await state.update_data(price=int(msg.text))
    answer = income.new_price(await state.get_data())
    await state.clear()
    await msg.answer(text=f"Назначена новая цена: {answer} руб.", reply_markup=keyboard.keyboard)

# -------------------------------------------------------------------------------

        ##################### Добавление денег в базу ######################

@router.message(F.text.in_(['Забор гор', 'Забор обл',
                            'Ложн гор', 'Ложн обл', 'Дист наст']),
                StateFilter(default_state))
async def add_money(msg: Message):
        answer = income.add_income_or_withdraw({'telegram_id': msg.from_user.id,
                                                    'title': msg.text,
                                                    'tag': 'my'
                                                    })
        await msg.answer(text=answer, reply_markup=keyboard.keyboard)


@router.message(F.text.in_(['Заказ гор', 'Заказ обл',
                            'Миостим гор', 'Миостим обл']),
                StateFilter(default_state))
async def choose_pay_method(msg: Message, state: FSMContext):
    await msg.answer(text="Выберите метод оплаты", reply_markup=keyboard.pay_keyboard)
    await state.set_state(FSMInputIncome.qr_or_cash)
    await state.update_data(telegram_id=msg.from_user.id, title=msg.text)


@router.message(StateFilter(FSMInputIncome.qr_or_cash), F.text == "QR-код")
async def pay_by_qr(msg: Message, state: FSMContext):
    await state.update_data(tag='my')
    answer = income.add_income_or_withdraw(await state.get_data())
    await state.clear()
    await msg.answer(text=answer, reply_markup=keyboard.keyboard)


@router.message(StateFilter(FSMInputIncome.qr_or_cash), F.text == "Наличные")
async def pay_in_cash(msg: Message, state: FSMContext):
    await state.update_data(tag='cash')
    await msg.answer(text="Введите сумму наличными")
    await state.set_state(FSMInputIncome.input_amount)


@router.message(StateFilter(FSMInputIncome.input_amount), F.text.regexp(r'[\d{2, 6}]'))
async def input_cash(msg: Message, state: FSMContext):
    await state.update_data(amount=int(msg.text))
    answer = income.add_income_or_withdraw(await state.get_data())
    await state.clear()
    await msg.answer(text=answer, reply_markup=keyboard.keyboard)

# ----------------------------------------------------------------------------------

##################### Ввод произвольной суммы ######################

@router.message(F.text == 'Ввести вручную', StateFilter(default_state))
async def manual_input(msg: Message, state: FSMContext):
        await state.set_state(FSMInputIncome.input_amount)
        await state.update_data(telegram_id=msg.from_user.id, title='Дополнительно', tag='extra')
        await msg.answer(text="Введите сумму наличными")

# -------------------------------------------------------------------------------------


@router.message(Command(commands=["account"]), StateFilter(default_state))
async def account_balance(msg: Message):
    answer = income.show_budget(msg.from_user.id)
    await msg.answer(text=f"Получено наличными: {answer.cash} руб.\n"
                          f"Мой заработок: {answer.my} руб.\n"
                          f"Дополнительно заработано: {answer.extra} руб.\n"
                          f"К сдаче {answer.to_return} руб.\n"
                          f"Итого моих: {answer.total_my} руб\n"
                          f"Итого снято {answer.withdrawal} руб.\n",
                          reply_markup=keyboard.keyboard)


@router.message(Command(commands=["help"]), StateFilter(default_state))
async def show_help(msg: Message):
    await msg.answer(text=LEXICON_RU["help_txt"])


@router.message(F.text == 'Отменить', ~StateFilter(default_state))
async def state_cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text='Действие отменено', reply_markup=keyboard.keyboard)

@router.message(Command(commands=["clear_month"]), StateFilter(default_state))
async def clear_month(msg: Message):
    answer = income.clear_month()
    await msg.answer(answer)

@router.message(Command(commands=["remove_last"]), StateFilter(default_state))
async def remove_last(msg: Message):
    answer = income.remove_last()
    await msg.answer(answer)

@router.message(StateFilter(default_state))
async def other(msg: Message):
    await msg.answer(text="Моя твоя не понимать."
                          "Для справки по командам отправьте /help ")
