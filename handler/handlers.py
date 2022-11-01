from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from keyboard.keyboard import *
from state.states import * 
from bot_init import bot

from message.message_handlers import *
from DB.db2 import *

from keyboard.keyboard_bu_inline import *


async def add_word(message: types.Message, state: FSMContext):
    """ Начинаем машину состояния и спрашиваем первое слово или фразу """

    answer = message.text

    dict_word = {
        "metod": "",
        "rus": "",
        "eng": ""
    }
    await state.update_data(dict_word)
    
    match answer:
        case "Добавить слово ->":
            await state.update_data(
                    {"metod": "word"})

        case "Добавить фразу ->":
            await state.update_data(
                    {"metod": "phrase"})
    
    data = await state.get_data()
    metod = data.get("metod")

    await bot.send_message(message.from_user.id, f"add_word {handlers_dict[f'add_{metod}_first']}")
    await bot.delete_message(message.chat.id, message.message_id)

    await QuestionParams.add_word_first.set()


async def add_word_first(message: types.Message, state: FSMContext):
    """ Записываем первое слово или фразу и спрашиваем второе """

    answer = message.text

    await state.update_data(
            {"rus": answer})

    data = await state.get_data()
    metod = data.get("metod")

    await bot.send_message(message.from_user.id, f"add_word_first {handlers_dict[f'add_{metod}_last']}")

    await QuestionParams.add_word_last.set()


async def add_word_last(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    answer = message.text

    await state.update_data(
            {"eng": answer})

    # В этом участке кода я буду делать запись в базу
    data = await state.get_data()
    wodr_rus = data.get("rus")
    wodr_eng = data.get("eng")

    data_base(wodr_rus,wodr_eng)

    data = await state.get_data()
    metod = data.get("metod")

    button = ["Нет", "Да"]
    keyboard_quit = Keyboard(button)
    
    await bot.send_message(message.from_user.id, f"add_word_replay Пара {wodr_rus} - {wodr_eng} была добавлена\n"
                                                f"{handlers_dict[f'add_{metod}_quit']}",
                                reply_markup=keyboard_quit.create_keyboadr())

    await QuestionParams.add_word_quit.set()


async def add_word_quit(message: types.Message, state: FSMContext):
    """ Или возвращаемся на начало или выводим на главное меню """

    answer = message.text

    match answer:
        case "Нет":
            await state.finish()

            button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест слова ->",
                      "Пройти тест фразы ->", "Повторение ->", "Настройки ->",
                      "Яблоко", "Apple"]
            keyboard_start = Keyboard(button)
            await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                   reply_markup=keyboard_start.create_keyboadr())
            await bot.delete_message(message.chat.id, message.message_id)

        case "Да":
            data = await state.get_data()
            metod = data.get("metod")

            await bot.send_message(message.from_user.id, f"{handlers_dict[f'add_{metod}_first']}",
                                reply_markup=types.ReplyKeyboardRemove())

            await QuestionParams.add_word_first.set()

async def start_test(message: types.Message, state: FSMContext):
    """ Записываем первое слово или фразу и спрашиваем второе """

    await bot.send_message(message.from_user.id, f"start_test {handlers_dict[f'start_test_word']}",
                           reply_markup=keyboard_choose())


async def question_test(message: types.Message, state: FSMContext):
    """ Записываем первое слово или фразу и спрашиваем второе """

    await bot.send_message(message.from_user.id, f"Как переводится ")

    await QuestionParams.add_word_first.set()






def register_handler_command(dp: Dispatcher):
    """Тут собраны все обработчики для функций выше"""

    dp.register_message_handler(add_word, Text(equals="Добавить слово ->"))
    dp.register_message_handler(add_word, Text(equals="Добавить фразу ->"))
    dp.register_message_handler(question_test, Text(equals="Начать ->"))

    dp.register_message_handler(start_test, Text(equals="Пройти тест: слова ->"))

    dp.register_message_handler(add_word_first, state=QuestionParams.add_word_first)
    dp.register_message_handler(add_word_last, state=QuestionParams.add_word_last)
    dp.register_message_handler(add_word_quit, state=QuestionParams.add_word_quit)






