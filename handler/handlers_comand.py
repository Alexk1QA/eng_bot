from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from message import message_handlers
from keyboard.keyboard import *
from bot_init import bot

from DB import db2


async def start(message: types.Message):
    """Стартовая функция"""

    button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
              "Пройти тест: фразы ->", "Повторение ->", "Настройки ->",
              "Яблоко", "Apple"]
    keyboard_start = Keyboard(button)

    await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['start']}",
                           reply_markup=keyboard_start.create_keyboadr())
    await bot.delete_message(message.chat.id, message.message_id)

    create_table = db2.DB(f"id_{message.from_user.id}")
    create_table.create_table()

    param_questions = "param_questions"
    try:
        if int(create_table.select_data(param_questions)[0][0]) == 10:
            pass

    except Exception as ex:
        create_table.insert_settings(3, 65)


async def info(message: types.Message):
    """Функция справки"""

    button = ["Главное меню"]
    keyboard_info = Keyboard(button)

    await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['info']}",
                           reply_markup=keyboard_info.create_keyboadr())


def register_handler_comands_command(dp: Dispatcher):
    """Тут собраны все обработчики для функций выше"""

    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(start, Text(equals="Главное меню"))
    dp.register_message_handler(info, commands=["info"])
