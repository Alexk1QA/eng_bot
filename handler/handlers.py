from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from message.message_handlers import *
from aiogram import types, Dispatcher
from keyboard.keyboard import *
from state.states import *
from func.func_bu import *
from bot_init import bot
from DB import db2


async def add_word(message: types.Message, state: FSMContext):
    """ Начинаем машину состояния и спрашиваем первое слово или фразу """

    answer = message.text

    match answer:
        case "Добавить слово ->":
            await state.update_data(method_add_data="word")

        case "Добавить фразу ->":
            await state.update_data(method_add_data="phrase")

    state_data = await state.get_data()
    method_add_data = state_data["method_add_data"]

    await bot.send_message(message.from_user.id, f"add_word {handlers_dict[f'add_{method_add_data}_first']}")
    await bot.delete_message(message.chat.id, message.message_id)

    await QuestionParams.add_word_first.set()


async def add_word_first(message: types.Message, state: FSMContext):
    """ Записываем первое слово или фразу и спрашиваем второе """

    answer = message.text

    await state.update_data(rus_add_data=answer)

    state_data = await state.get_data()
    method_add_data = state_data["method_add_data"]

    await bot.send_message(message.from_user.id, f"add_word_first {handlers_dict[f'add_{method_add_data}_last']}")

    await QuestionParams.add_word_last.set()


async def add_word_last(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    answer = message.text

    await state.update_data(eng_add_data=answer)

    state_data = await state.get_data()

    # В этом участке кода я буду делать запись в базу
    rus_add_data = state_data["rus_add_data"]
    eng_add_data = state_data["eng_add_data"]
    method_add_data = state_data["method_add_data"]

    create_table = db2.DB(message.from_user.id)
    create_table.insert_data(method_add_data, rus_add_data, eng_add_data)

    button = ["Нет", "Да"]
    keyboard_quit = Keyboard(button)

    await bot.send_message(message.from_user.id, f"add_word_replay Пара {rus_add_data} - {eng_add_data} была добавлена"
                                                 f"\n{handlers_dict[f'add_{method_add_data}_quit']}",
                                                 reply_markup=keyboard_quit.create_keyboadr())

    await QuestionParams.add_word_quit.set()


async def add_word_quit(message: types.Message, state: FSMContext):
    """ Спрашиваем повторно ввод данных за ввод или переводим на главное меню """

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
            state_data = await state.get_data()
            method_add_data = state_data["method_add_data"]

            await bot.send_message(message.from_user.id, f"{handlers_dict[f'add_{method_add_data}_first']}",
                                   reply_markup=types.ReplyKeyboardRemove())

            await QuestionParams.add_word_first.set()


async def start_test(message: types.Message, state: FSMContext):
    """ Начало машины состояния """

    answer = message.text

    create_table = db2.DB(message.from_user.id)
    create_table.create_table()

    param_questions = "param_questions"
    param_percent = "param_percent"

    await state.update_data(param_questions=int(create_table.select_data(param_questions)[0][0]))
    await state.update_data(param_percent=int(create_table.select_data(param_percent)[0][0]))
    await state.update_data(count_fails=0)
    await state.update_data(count_questions=0)
    await state.update_data(status_=0)

    await state.update_data(temp_method=answer)

    await state.update_data(list_fails=[])

    button = ["Начать ->"]

    keyboard_start_ = Keyboard(button)
    await bot.send_message(message.from_user.id, f".",
                           reply_markup=keyboard_start_.create_keyboadr())

    await bot.delete_message(message.chat.id, message.message_id)

    await bot.send_message(message.from_user.id, f"start_test {handlers_dict[f'start_test_word']}",
                           reply_markup=keyboard_choose(message.from_user.id))


async def question_test(message: types.Message, state: FSMContext):
    """ Тут мы сортируем слова по сроку который указал пользователь и вариант отображения слов
         1 - За посл неделю, 2 - За все время, 3 - рус --> англ, 4 - англ --> рус """

    answer = message.text

    state_data = await state.get_data()

    param_questions = int(state_data["param_questions"])
    param_percent = int(state_data["param_percent"])
    count_fails = int(state_data["count_fails"])
    count_questions = int(state_data["count_questions"])
    status_ = int(state_data["status_"])

    temp_method = state_data["temp_method"]

    match status_:
        case 0:
            pass

        case 1:
            origin_para = state_data["origin_para"]
            answer_state = state_data["answer_state"]
            list_fails = state_data["list_fails"]

            if count_questions < param_questions:

                if str(answer) == str(answer_state):
                    pass

                elif str(answer) != str(answer_state):

                    count_fails += 1
                    await state.update_data(count_fails=count_fails)
                    list_fails_ = [origin_para, answer]
                    list_fails.append(list_fails_)

                    await state.update_data(list_fails=list_fails)

            else:
                if str(answer) == str(answer_state):
                    pass

                elif str(answer) != str(answer_state):

                    count_fails += 1
                    await state.update_data(count_fails=count_fails)

                    list_fails_ = [origin_para, answer]
                    list_fails.append(list_fails_)
                    await state.update_data(list_fails=list_fails)

                max_percent_fails = 100 - param_percent
                # Вычисляем минимальный % для определения прохождения теста.
                # Пример: 100 - 70 - доступно для ошибок 30 %

                actual_percent = (count_fails / param_questions) * 100
                # Пример 3/10  * 100 = 30 %

                if count_fails == 0:

                    await bot.send_message(message.from_user.id,
                                           f"Тест пройден. Ваш процент ответов - 100%")

                else:
                    if actual_percent > max_percent_fails:

                        list_fails = state_data["list_fails"]

                        await bot.send_message(message.from_user.id,
                                               f"Тест НЕ пройден. Ваш процент ответов - "
                                               f"{str(100 - int(actual_percent))[0:5]}%")

                        await bot.send_message(message.from_user.id, f"Слова в которых допускались ошибки: "
                                                                     f"{message_(list_fails)}")

                        await state.finish()

                    elif actual_percent <= max_percent_fails:
                        await bot.send_message(message.from_user.id, f"Тест пройден. Ваш процент ответов - "
                                                                     f"{str(100 - int(actual_percent))[0:5]}%")

                        await bot.send_message(message.from_user.id, f"Слова в которых допускались ошибки: "
                                                                     f"{message_(list_fails)}")

                        await state.finish()

    # Вывод на главное меню после последнего вопроса
    if count_questions == param_questions:
        button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                  "Пройти тест: фразы ->", "Повторение ->", "Настройки ->",
                  "Яблоко", "Apple"]
        keyboard_start = Keyboard(button)

        await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                               reply_markup=keyboard_start.create_keyboadr())

    else:
        match temp_method:
            case "Пройти тест: слова ->":
                data_ = random_question("word", message.from_user.id)
                # example data_ --> # [3, ['Яблоко', 'Apple']]

                match data_[0]:
                    case int(3):
                        # "3": "рус --> англ "
                        await bot.send_message(message.from_user.id, f"Как переводится слово {data_[1][0]}")

                        await state.update_data(origin_para=data_[1])
                        await state.update_data(question_state=data_[1][0])
                        await state.update_data(answer_state=data_[1][1])

                        count_questions += 1
                        await state.update_data(count_questions=count_questions)

                        status_ = 1
                        await state.update_data(status_=status_)

                        await QuestionParams.question_test.set()

                    case int(4):
                        # "4": "англ --> рус "
                        await bot.send_message(message.from_user.id, f"Как переводится слово {data_[1][1]}")

                        await state.update_data(origin_para=data_[1])
                        await state.update_data(question_state=data_[1][1])
                        await state.update_data(answer_state=data_[1][0])

                        count_questions += 1
                        await state.update_data(count_questions=count_questions)

                        status_ = 1
                        await state.update_data(status_=status_)

                        await QuestionParams.question_test.set()

            case "Пройти тест: фразы ->":
                data_ = random_question("phrase", message.from_user.id)

                match data_[0]:
                    case int(3):
                        # "3": "рус --> англ "
                        await bot.send_message(message.from_user.id, f"Как переводится фраза {data_[1][0]}")

                        await state.update_data(origin_para=data_[1])
                        await state.update_data(question_state=data_[1][0])
                        await state.update_data(answer_state=data_[1][1])

                        count_questions += 1
                        await state.update_data(count_questions=count_questions)

                        status_ = 1
                        await state.update_data(status_=status_)

                        await QuestionParams.question_test.set()

                    case int(4):
                        # "4": "англ --> рус "
                        await bot.send_message(message.from_user.id, f"Как переводится фраза {data_[1][1]}")

                        await state.update_data(origin_para=data_[1])
                        await state.update_data(question_state=data_[1][1])
                        await state.update_data(answer_state=data_[1][0])

                        count_questions += 1
                        await state.update_data(count_questions=count_questions)

                        status_ = 1
                        await state.update_data(status_=status_)

                        await QuestionParams.question_test.set()


async def user_settings(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    create_table = db2.DB(message.from_user.id)
    # create_table.create_table()

    param_questions_ = "param_questions"
    param_percent_ = "param_percent"

    await state.update_data(user_settings_status=0)

    buttons = ["Вопросы", "Процент ошибок", "Назад"]

    keyboard_settings = Keyboard(buttons)

    await bot.send_message(message.from_user.id, f"user_settings {handlers_dict[f'user_settings']}\n\n"
                                                 f"Вопросы - {create_table.select_data(param_questions_)[0][0]}\n"
                                                 f"Процент - {create_table.select_data(param_percent_)[0][0]}\n",
                                                 reply_markup=keyboard_settings.create_keyboadr())

    await QuestionParams.user_settings_update.set()


async def user_settings_update(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    answer = message.text

    write_settings = db2.DB(message.from_user.id)

    state_data = await state.get_data()
    user_settings_status = int(state_data["user_settings_status"])

    match user_settings_status:
        case 0:
            match answer:

                case "Вопросы":
                    await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_q']}")

                    await state.update_data(user_settings_status=1)
                    await state.update_data(user_settings_update=answer)
                    await QuestionParams.user_settings_update.set()

                case "Процент ошибок":
                    await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_%']}")

                    await state.update_data(user_settings_status=1)
                    await state.update_data(user_settings_update=answer)
                    await QuestionParams.user_settings_update.set()

                case _:
                    user_settings_status = 1
                    await state.finish()

        case 1:
            try:
                answer = int(answer)

                user_settings_update = state_data["user_settings_update"]

                match user_settings_update:

                    case "Вопросы":
                        param_questions = "param_questions"

                        # write_settings.update_data(param_questions, answer)

                        await bot.send_message(message.from_user.id,
                                               f"{handlers_dict['user_settings_update_accept_q']} - {answer}%")

                        await state.finish()

                    case "Процент ошибок":
                        param_percent = "param_percent"

                        # write_settings.update_data(param_percent, answer)

                        await bot.send_message(message.from_user.id,
                                               f"{handlers_dict['user_settings_update_accept_%']} - {answer}%")

                        await state.finish()

            except Exception as ex:
                await bot.send_message(message.from_user.id, f"Вводите только целые числа")

                user_settings_status = 1
                await state.finish()

    if user_settings_status == 1:

        button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                                        "Пройти тест: фразы ->", "Повторение ->", "Настройки ->",
                                        "Яблоко", "Apple"]
        keyboard_start = Keyboard(button)

        await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                            reply_markup=keyboard_start.create_keyboadr())


def register_handler_command(dp: Dispatcher):

    dp.register_message_handler(add_word, Text(equals="Добавить слово ->"))
    dp.register_message_handler(add_word, Text(equals="Добавить фразу ->"))

    dp.register_message_handler(start_test, Text(equals="Пройти тест: слова ->"))
    dp.register_message_handler(start_test, Text(equals="Пройти тест: фразы ->"))

    dp.register_message_handler(add_word_first, state=QuestionParams.add_word_first)
    dp.register_message_handler(add_word_last, state=QuestionParams.add_word_last)
    dp.register_message_handler(add_word_quit, state=QuestionParams.add_word_quit)

    dp.register_message_handler(question_test, Text(equals="Начать ->"))

    dp.register_message_handler(user_settings, Text(equals="Настройки ->"))
    dp.register_message_handler(user_settings_update, state=QuestionParams.user_settings_update)

    dp.register_message_handler(question_test, state=QuestionParams.question_test)