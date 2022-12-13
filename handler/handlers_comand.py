from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from message import message_handlers
from keyboard.buttons_menu import *
from log.logging import logger_
from keyboard.keyboard import *
from bot_init import bot
from DB import db2
import json


async def start(message: types.Message):
    """ Start func """

    keyboard_start = Keyboard(buttons_main_menu)

    await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['start']}",
                           reply_markup=keyboard_start.create_keyboard(3))
    await bot.delete_message(message.chat.id, message.message_id)

    data_base = db2.DB(message.from_user.id)
    data_base.create_table()

    try:
        check = int(data_base.select_data_(column_="keyboard_boot")[0][0])

        if check == 0 or check == 1:
            pass

    except Exception as ex:
        logger_(message.from_user.id, f"file: handlers_command/start /// {ex}")

        params_user = json.dumps({
            "param_questions": 10,
            "param_percent": 50,
            "param_day": 7,
            "mode_questions": "rus",
            "mode_add_word": "ask",
        })

        status_ = 1

        butt_dict = json.dumps({
            "1": "За период ",
            "2": "За все время ✅",
            "3": "англ --> рус ✅",
            "4": "рус --> англ "
        })

        butt_dict_upd = json.dumps({
            "1": "За период ",
            "2": "За все время ",
            "3": "англ --> рус ",
            "4": "рус --> англ "
        })

        data_base.insert_settings(params_user, status_, butt_dict, butt_dict_upd)


async def info(message: types.Message):
    """ Func info"""

    button = ["Главное меню"]
    keyboard_info = Keyboard(button)

    await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['info']}",
                           reply_markup=keyboard_info.create_keyboard(3))


def register_handler_commands_command(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(start, Text(equals="Главное меню"))
    dp.register_message_handler(info, commands=["info"])
