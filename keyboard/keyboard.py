from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


zakaz_gorod_button = KeyboardButton(text="Заказ гор")
zabor_gorod_button = KeyboardButton(text="Забор гор")
zakaz_obl_button = KeyboardButton(text="Заказ обл")
zabor_obl_button = KeyboardButton(text="Забор обл")
miostim_gorod_button = KeyboardButton(text="Миостим гор")
miostim_obl_button = KeyboardButton(text="Миостим обл")
lozh_gorod_button = KeyboardButton(text="Ложн гор")
lozh_obl_button = KeyboardButton(text=f"Ложн обл")
distanz_button = KeyboardButton(text=f"Дист наст")
withdraw_button = KeyboardButton(text=f"Списать")
manual_input_button = KeyboardButton(text='Ввести вручную')
qr_button = KeyboardButton(text='QR-код')
cash_button = KeyboardButton(text='Наличные')
cancel_button = KeyboardButton(text='Отменить')



keyboard = ReplyKeyboardMarkup(keyboard=[
    [zakaz_gorod_button, zabor_gorod_button],
    [zakaz_obl_button, zabor_obl_button],
    [miostim_gorod_button, miostim_obl_button],
    [lozh_gorod_button, lozh_obl_button],
    [distanz_button, manual_input_button],
    [withdraw_button]
], resize_keyboard=True)

pay_keyboard = ReplyKeyboardMarkup(keyboard=[[qr_button, cash_button], [cancel_button]], resize_keyboard=True)
