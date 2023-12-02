from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


zakaz_gorod_button = KeyboardButton(text="Заказ гор")
zabor_gorod_button = KeyboardButton(text="Забор гор")
zakaz_obl_button = KeyboardButton(text="Заказ обл")
zabor_obl_button = KeyboardButton(text="Забор обл")
lozh_gorod_button = KeyboardButton(text="Ложн гор")
lozh_obl_button = KeyboardButton(text=f"Ложн обл")
distanz_button = KeyboardButton(text=f"Дист наст")
withdraw_button = KeyboardButton(text=f"Списать")

keyboard = ReplyKeyboardMarkup(keyboard=[
    [zakaz_gorod_button, zabor_gorod_button],
    [zakaz_obl_button, zabor_obl_button],
    [lozh_gorod_button, lozh_obl_button],
    [distanz_button, withdraw_button]], resize_keyboard=True)
