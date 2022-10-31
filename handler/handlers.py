from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from keyboard.keyboard import *
from state.states import *
from bot_init import bot

from message.message_handlers import *
from DB.db2 import *

wodr_rus = "Яблоко"
wodr_eng = "Apple"

data_base(wodr_rus,wodr_eng)


dict_ = {}


async def add_word(message: types.Message, state: FSMContext):
    """ Начинаем машину состояния и спрашиваем первое словов """

    dict_word = {
        "rus": "",
        "eng": ""
    }
    await state.update_data(dict_word)

    await bot.send_message(message.from_user.id, f"add_word {handlers_dict['add_word_first']}")
    await bot.delete_message(message.chat.id, message.message_id)


    await QuestionParams.add_word_first.set()


async def add_word_first(message: types.Message, state: FSMContext):
    """ Записываем первое слово и спрашиваем второе """

    answer = message.text

    await state.update_data(
            {"rus": answer})

    await bot.send_message(message.from_user.id, f"add_word_first {handlers_dict['add_word_last']}")

    await QuestionParams.add_word_last.set()


async def add_word_last(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово """

    answer = message.text

    await state.update_data(
            {"eng": answer})

    # В этом участке кода я буду делать запись в базу
    data = await state.get_data()
    wodr_rus = data.get("rus")
    wodr_eng = data.get("eng")

    # a = dict(name=f'{wodr_rus}', value=f'{wodr_eng}')
    # add_words(a)

    print(wodr_rus,wodr_eng)

    data_base(wodr_rus,wodr_eng)

    button = ["Нет", "Да"]
    keyboard_quit = Keyboard(button)

    await bot.send_message(message.from_user.id, f"add_word_replay Слово {wodr_rus} - {wodr_eng} было добавлено\n"
                                                 f"{handlers_dict['add_word_replay']}",
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
            print(dict_)

        case "Да":
            await bot.send_message(message.from_user.id, f"add_word {handlers_dict['add_word_first']}",
                                   reply_markup=types.ReplyKeyboardRemove())
            await QuestionParams.add_word_first.set()
            print(dict_)


def register_handler_command(dp: Dispatcher):
    """Тут собраны все обработчики для функций выше"""

    dp.register_message_handler(add_word, Text(equals="Добавить слово ->"))

    dp.register_message_handler(add_word_first, state=QuestionParams.add_word_first)
    dp.register_message_handler(add_word_last, state=QuestionParams.add_word_last)
    # dp.register_message_handler(add_word_replay, state=QuestionParams.add_word_replay)
    dp.register_message_handler(add_word_quit, state=QuestionParams.add_word_quit)






