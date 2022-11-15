from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from message import message_handlers
from keyboard.keyboard import *
from bot_init import bot
from DB import db2


async def start(message: types.Message):
    """Стартовая функция"""

    button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
              "Пройти тест: фразы ->", "Повторение слова ->", "Настройки ->"]
    keyboard_start = Keyboard(button)

    await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['start']}",
                           reply_markup=keyboard_start.create_keyboadr(3))
    await bot.delete_message(message.chat.id, message.message_id)

    create_table = db2.DB(message.from_user.id)
    create_table.create_table()

    param_questions = "param_questions"

    try:
        if int(create_table.select_data(param_questions)[0][0]) == 10:
            pass

    except Exception as ex:
        print(ex)

        param_questions = 3
        param_percent = 50
        status = 1
        default_day = 7
        param_answer = 0

        butt_dict = {
            "1": "За период ",
            "2": "За все время ✅",
            "3": "рус --> англ ✅",
            "4": "англ --> рус "
        }

        butt_dict_upd = {
            "1": "За период ",
            "2": "За все время ",
            "3": "рус --> англ ",
            "4": "англ --> рус "
        }

        create_table.insert_settings(param_questions, param_percent, status,
                                     default_day, param_answer, butt_dict, butt_dict_upd)


async def info(message: types.Message):
    """Функция справки"""

    button = ["Главное меню"]
    keyboard_info = Keyboard(button)

    await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['info']}",
                           reply_markup=keyboard_info.create_keyboadr(3))


def register_handler_commands_command(dp: Dispatcher):
    """Тут собраны все обработчики для функций выше"""

    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(start, Text(equals="Главное меню"))
    dp.register_message_handler(info, commands=["info"])
