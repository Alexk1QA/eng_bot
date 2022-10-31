from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_Back_Menu = KeyboardButton("Главное меню")

keyboard_Back_Menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_Back_Menu)


# button_new = KeyboardButton("Новые")
# button_BU = KeyboardButton("Б/У")
#
# keyboard_NewOrBU = ReplyKeyboardMarkup(resize_keyboard=True).add(button_new, button_BU)

class Keyboard:

    def __init__(self, list_button):
        self.list_button = list_button

    def create_keyboadr(self):
        keyboard_NewOrBU = ReplyKeyboardMarkup(resize_keyboard=True).add()

        for i in self.list_button:
            button = KeyboardButton(i)
            keyboard_NewOrBU.insert(button)

        return keyboard_NewOrBU
