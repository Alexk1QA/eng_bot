from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboard.keyboard import *
from bot_init import bot
from DB import db2


async def start(message: types.Message):
    """Стартовая функция"""

    print("---")
    if message.from_user.id == 26750009 or message.from_user.id == 1882554481:
        # await bot.send_message(message.from_user.id, f"Ты что, столько времени тратить")

        button = ["Я виновата", "Я не виновата"]
        keyboard_quit = Keyboard(button)

        await bot.send_message(message.from_user.id,
                               f"Ты что, столько времени тратить. 2 мин это ж пипец как много.\n"
                               f"Выбери правильный вариант )))",
                               reply_markup=keyboard_quit.create_keyboadr())


async def ignore(message: types.Message):

    answer = message.text

    create_table = db2.DB(message.from_user.id)
    create_table.create_table()

    status = 1
    butt_dict = {
        "1": "За посл неделю ✅"
    }

    butt_dict_upd = {
        "1": "За посл неделю "
    }

    create_table.insert_settings(3, 50, status, butt_dict, butt_dict_upd)

    if answer == "Я виновата":
        await bot.send_message(message.from_user.id, f"Я подумаю, разблокировать тебя или нет) ")

    elif answer == "Я не виновата":
        await bot.send_message(message.from_user.id, f"Полагаю тебе стоит еще подумать) ")


def register_handler_commands_command_ignore(dp: Dispatcher):
    """Тут собраны все обработчики для функций выше"""

    dp.register_message_handler(start, commands=["start"])

    dp.register_message_handler(ignore, Text(equals="Я виновата"))
    dp.register_message_handler(ignore, Text(equals="Я не виновата"))