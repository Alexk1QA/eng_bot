from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class Keyboard:
    def __init__(self, list_button):
        self.list_button = list_button

    def create_keyboard(self, row_width_):
        keyboard_NewOrBU = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width_).add()

        for i in self.list_button:
            button = KeyboardButton(i)
            keyboard_NewOrBU.insert(button)

        return keyboard_NewOrBU
