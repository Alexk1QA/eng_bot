from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class Keyboard:

    def __init__(self, list_button):
        self.list_button = list_button

    def create_keyboadr(self):
        keyboard_NewOrBU = ReplyKeyboardMarkup(resize_keyboard=True).add()

        for i in self.list_button:
            button = KeyboardButton(i)
            keyboard_NewOrBU.insert(button)

        return keyboard_NewOrBU
