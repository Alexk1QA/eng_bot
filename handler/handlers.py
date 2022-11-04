from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher

# import DB.db2
from keyboard.keyboard import *
from state.states import * 
from bot_init import bot
from func.func_bu import *



from message.message_handlers import *
# from DB.db2 import *
from DB import db2
from keyboard.keyboard_bu_inline import *
from aiogram.types import CallbackQuery


async def add_word(message: types.Message, state: FSMContext):
    """ Начинаем машину состояния и спрашиваем первое слово или фразу """

    answer = message.text

    dict_param = {
        "method": "",
        "rus": "",
        "eng": "",

        "temp_translate": "",
        "status": "",

        "temp_method": "",
        "param_questions": "",
        "param_percent": "",
        "count_fails": "",
        "count_questions": ""
    }
    await state.update_data(dict_param)
    
    match answer:
        case "Добавить слово ->":
            await state.update_data(
                    {"method": "word"})

        case "Добавить фразу ->":
            await state.update_data(
                    {"method": "phrase"})
    
    data = await state.get_data()
    method = data.get("method")

    await bot.send_message(message.from_user.id, f"add_word {handlers_dict[f'add_{method}_first']}")
    await bot.delete_message(message.chat.id, message.message_id)

    await QuestionParams.add_word_first.set()


async def add_word_first(message: types.Message, state: FSMContext):
    """ Записываем первое слово или фразу и спрашиваем второе """

    answer = message.text

    await state.update_data(
            {"rus": answer})

    data = await state.get_data()
    method = data.get("method")

    await bot.send_message(message.from_user.id, f"add_word_first {handlers_dict[f'add_{method}_last']}")

    await QuestionParams.add_word_last.set()


async def add_word_last(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    answer = message.text

    await state.update_data(
            {"eng": answer})

    data = await state.get_data()

    # В этом участке кода я буду делать запись в базу
    wodr_rus = data.get("rus")
    wodr_eng = data.get("eng")
    method = data.get("method")

    # data_base(wodr_rus,wodr_eng)
    create_table = db2.DB(method)
    create_table.create_table()
    create_table.insert_data(wodr_rus, wodr_eng)

    button = ["Нет", "Да"]
    keyboard_quit = Keyboard(button)
    
    await bot.send_message(message.from_user.id, f"add_word_replay Пара {wodr_rus} - {wodr_eng} была добавлена\n"
                                                f"{handlers_dict[f'add_{method}_quit']}",
                                reply_markup=keyboard_quit.create_keyboadr())

    await QuestionParams.add_word_quit.set()


async def add_word_quit(message: types.Message, state: FSMContext):
    """ Или возвращаемся на начало или выводим на главное меню """

    answer = message.text

    match answer:
        case "Нет":
            await state.finish()

            button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                      "Пройти тест: фразы ->", "Повторение ->", "Настройки ->",
                      "Яблоко", "Apple"]
            keyboard_start = Keyboard(button)
            await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                   reply_markup=keyboard_start.create_keyboadr())
            await bot.delete_message(message.chat.id, message.message_id)

        case "Да":
            data = await state.get_data()
            method = data.get("method")

            await bot.send_message(message.from_user.id, f"{handlers_dict[f'add_{method}_first']}",
                                reply_markup=types.ReplyKeyboardRemove())

            await QuestionParams.add_word_first.set()


async def start_test(message: types.Message, state: FSMContext):
    """ Записываем первое слово или фразу и спрашиваем второе """

    answer = message.text

    await state.update_data(
        {"param_questions": 3})
    await state.update_data(
        {"param_percent": 75})
    await state.update_data(
        {"count_fails": 0})
    await state.update_data(
        {"count_questions": 0})
    await state.update_data(
        {"status": 0})



    await state.update_data(
                    {"temp_method": answer})


    data = await state.get_data()
    temp_method = data.get("temp_method")
    print(temp_method)

    button = ["Начать ->"]
    keyboard_start_ = Keyboard(button)
    await bot.send_message(message.from_user.id, f".",
                       reply_markup=keyboard_start_.create_keyboadr())
    await bot.delete_message(message.chat.id, message.message_id)

    await bot.send_message(message.from_user.id, f"start_test {handlers_dict[f'start_test_word']}",
                           reply_markup=keyboard_choose())


async def question_test(message: types.Message, state: FSMContext):
    """ Тут мы сортируем слова по сроку который указал пользователь и вариант отображения слов
         1 - За посл неделю, 2 - За все время, 3 - рус --> англ, 4 - англ --> рус """

    answer = message.text

    data = await state.get_data()
    temp_method = data.get("temp_method")

    param_questions = int(data.get("param_questions"))
    param_percent = int(data.get("param_percent"))
    count_fails = int(data.get("count_fails"))
    count_questions = int(data.get("count_questions"))
    print("--- --- ---")

    temp_para = data.get("temp_para")
    temp_translate = data.get("temp_translate")

    status = int(data.get("status"))

    list_para = []
    list_fails = []

    match status:
        case 0:
            pass

        case 1:
            print(temp_translate)
            print(answer)
            if count_questions < param_questions:
                if answer == "Начать ->":
                    # await bot.answer_callback_query(call.id, text='Правильно')
                    # await call.message.edit_reply_markup()
                    pass

                elif str(answer) == str(temp_translate):
                    pass

                elif str(answer) != str(temp_translate):
                    count_fails += 1
                    await state.update_data(
                        {"count_fails": count_fails})
                    list_fails.append(temp_translate)
                    list_para.append(temp_para)
                    print(list_fails, list_para)

            else:
                count_fails += 1
                await state.update_data(
                    {"count_fails": count_fails})
                print("2 else")
                # Вызываем функцию для определения %
                # Пишем, сообщение - Правильный перевод такой - Ваш такой

                # ((75 / 100) * 10 ) - 10 = 2.5
                actual_percent = (count_fails / param_questions) * 100

                if actual_percent > param_percent:
                    await bot.send_message(message.from_user.id,
                                           f"Тест пройден. Ваш процент ответов - {str(actual_percent)[0:5]}%")

                    await bot.send_message(message.from_user.id, f"Слова в которых допускались ошибки: "
                                                                 f"{list_fails}, {list_para}")

                    await state.finish()


                elif actual_percent < param_percent:
                    await bot.send_message(message.from_user.id,
                                           f"Тест НЕ пройден. Ваш процент ответов - {str(actual_percent)[0:5]}%")

                    await bot.send_message(message.from_user.id, f"Слова в которых допускались ошибки: "
                                                                 f"{list_fails}, {list_para}")

                    await state.finish()

    if count_questions == param_questions:
        button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                  "Пройти тест: фразы ->", "Повторение ->", "Настройки ->",
                  "Яблоко", "Apple"]
        keyboard_start = Keyboard(button)
        await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                               reply_markup=keyboard_start.create_keyboadr())
        pass
    else:
        match temp_method:
            case "Пройти тест: слова ->":
                data_ = random_question("word")
# example data_ --> [2, ('Яблоко', 'Apple', 'Thu Nov  3 14:03:26 2022'), ('3333', '44444', 'Thu Nov  3 14:56:17 2022')]

                match data_[0]:
                    case int(3):
                        await bot.send_message(message.from_user.id, f"Как переводится слово {data_[1][0]}")
                        await state.update_data(
                            {"temp_translate": data_[1][1]})
                        count_questions += 1
                        await state.update_data(
                            {"count_questions": count_questions})
                        await state.update_data(
                            {"status": 1})
                        await QuestionParams.question_test.set()

                    case int(4):
                        await bot.send_message(message.from_user.id, f"Как переводится слово {data_[1][1]}")
                        await state.update_data(
                            {"temp_translate": data_[1][0]})
                        count_questions += 1
                        await state.update_data(
                            {"count_questions": count_questions})
                        await state.update_data(
                            {"status": 1})
                        await QuestionParams.question_test.set()

            case "Пройти тест: фразы ->":
                data_ = random_question("phrase")

                match data_[0]:
                    case int(3):
                        await bot.send_message(message.from_user.id, f"Как переводится слово {data_[1][0]}")
                        await state.update_data(
                            {"temp_translate": data_[1][1]})
                        count_questions += 1
                        await state.update_data(
                            {"count_questions": count_questions})
                        await state.update_data(
                            {"status": 1})
                        await QuestionParams.question_test.set()

                    case int(4):
                        await bot.send_message(message.from_user.id, f"Как переводится слово {data_[1][1]}")
                        await state.update_data(
                            {"temp_translate": data_[1][0]})
                        count_questions += 1
                        await state.update_data(
                            {"count_questions": count_questions})
                        await state.update_data(
                            {"status": 1})
                        await QuestionParams.question_test.set()

        print("")
        print(f"param_questions - {param_questions}\n"
              f"param_percent - {param_percent}\n"
              f"count_fails - {count_fails}\n"
              f"count_questions - {count_questions}\n"
              f"status - {status}")

# async def answer_test(message: types.Message, state: FSMContext):
#     """ Записываем первое слово или фразу и спрашиваем второе """
#
#     answer = message.text
#
#     # Добавить настройку счетчика в настройках
#     # (4/10) * 100 = 40%
#
#     data = await state.get_data()
#
#     param_questions = int(data.get("param_questions"))
#     param_percent = int(data.get("param_percent"))
#     count_fails = int(data.get("count_fails"))
#     count_questions = int(data.get("count_questions"))
#
#
#     temp_para = data.get("temp_para")
#     temp_translate = data.get("temp_translate")
#
#     list_para = []
#     list_fails = []
#
#     if count_questions < param_questions:
#
#         if temp_translate == answer:
#             count_questions += 1
#             await QuestionParams.question_test.set()
#         else:
#             count_fails += 1
#             count_questions += 1
#             list_fails.append(temp_translate)
#             list_para.append(temp_para)
#             await QuestionParams.question_test.set()
#     else:
#         # Вызываем функцию для определения %
#         # Пишем, сообщение - Правильный перевод такой - Ваш такой
#
#         # ((75 / 100) * 10 ) - 10 = 2.5
#         actual_percent = (count_fails / param_questions) * 100
#
#         if actual_percent > param_percent:
#             await bot.send_message(message.from_user.id, f"Тест пройден. Ваш процент ответов - {actual_percent}%")
#
#             await bot.send_message(message.from_user.id, f"Слова в которых допускались ошибки: "
#                                                          f"{list_fails}, {list_para}")
#
#             await state.finish()
#
#
#         elif actual_percent < param_percent:
#             await bot.send_message(message.from_user.id, f"Тест НЕ пройден. Ваш процент ответов - {actual_percent}%")
#
#             await bot.send_message(message.from_user.id, f"Слова в которых допускались ошибки: "
#                                                          f"{list_fails}, {list_para}")
#
#             await state.finish()
#
#     # Так же сделать процентовку
#         if count_questions < param_questions:
#             count_questions += 1
#             await QuestionParams.question_test.set()
#
#         elif count_questions == param_questions:
#
#             if param_percent < 80:
#
#                 await bot.send_message(message.from_user.id, f"Тест пройден ")
#                 await state.finish()
#         else:
#             count_questions += 1
#             count_fails =+ 1
#             await QuestionParams.question_test.set()
#
#         await bot.send_message(message.from_user.id, f"Как переводится - - -")
#
#         await QuestionParams.question_test.set()





def register_handler_command(dp: Dispatcher):
    """Тут собраны все обработчики для функций выше"""

    dp.register_message_handler(add_word, Text(equals="Добавить слово ->"))
    dp.register_message_handler(add_word, Text(equals="Добавить фразу ->"))

    dp.register_message_handler(start_test, Text(equals="Пройти тест: слова ->"))

    dp.register_message_handler(add_word_first, state=QuestionParams.add_word_first)
    dp.register_message_handler(add_word_last, state=QuestionParams.add_word_last)
    dp.register_message_handler(add_word_quit, state=QuestionParams.add_word_quit)

    dp.register_message_handler(question_test, Text(equals="Начать ->"))

    dp.register_message_handler(question_test, state=QuestionParams.question_test)
    # dp.register_message_handler(answer_test, state=QuestionParams.answer_test)






