from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from message.message_handlers import *
from aiogram import types, Dispatcher
from keyboard.buttons_menu import *
from log.logging import logger_
from keyboard.keyboard import *
from state.states import *
from func.func_bu import *
from bot_init import bot
from DB import db2


async def add_word(message: types.Message, state: FSMContext):
    """ Начинаем машину состояния и спрашиваем первое слово или фразу """

    data_base = db2.DB(message.from_user.id)

    mode_questions = json.loads(data_base.select_data_(
        column_="params_user", where_clmn="id", where_data=1)[0][0])["mode_questions"]

    await state.update_data(mode_questions=mode_questions)

    await bot.delete_message(message.chat.id, message.message_id)

    answer = message.text

    match answer:
        case "Добавить слово ->":
            await state.update_data(method_add_data="word")

        case "Добавить фразу ->":
            await state.update_data(method_add_data="phrase")

    state_data = await state.get_data()

    keyboard_cancel = Keyboard(["Отмена ->"])

    mode_add_word = json.loads(data_base.select_data_(
        column_="params_user", where_clmn="id", where_data=1)[0][0])["mode_add_word"]
    await state.update_data(mode_add_word=mode_add_word)

    del_msg_1 = 0
    match mode_add_word:
        case "ask":
            del_msg_1 = await bot.send_message(message.from_user.id, f"Режим добавления слов: Ручной")

        case "auto":
            del_msg_1 = await bot.send_message(message.from_user.id, f"Режим добавления слов: Автоматический")

    match state_data["mode_questions"]:
        case "rus":
            del_msg_2 = await bot.send_message(message.from_user.id,
                                               f"""{handlers_dict[f'add_{state_data["method_add_data"]}_first']}""",
                                               reply_markup=keyboard_cancel.create_keyboard(3))

            await state.update_data(list_delete=[message.message_id, del_msg_1.message_id, del_msg_2.message_id])
            await QuestionParams.add_word_first.set()

        case "eng":
            del_msg_2 = await bot.send_message(message.from_user.id,
                                               f"""{handlers_dict[f'add_{state_data["method_add_data"]}_last']}""",
                                               reply_markup=keyboard_cancel.create_keyboard(3))

            await state.update_data(list_delete=[message.message_id, del_msg_1.message_id, del_msg_2.message_id])
            await QuestionParams.add_word_first.set()


async def add_word_first(message: types.Message, state: FSMContext):
    """ Записываем первое слово или фразу и спрашиваем второе """

    answer = message.text

    data_base = db2.DB(message.from_user.id)

    if answer == "Отмена ->" or answer == "Готово ->":
        await bot.delete_message(message.chat.id, message.message_id)

        keyboard_start = Keyboard(buttons_main_menu)

        await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                               reply_markup=keyboard_start.create_keyboard(3))

        finally_state_data = await state.get_data()

        await delete_message(message.chat.id, finally_state_data["list_delete"])

        await state.finish()

    else:
        state_data = await state.get_data()

        list_delete = state_data["list_delete"]

        method_add_data = state_data["method_add_data"]
        # example -> word
        mode_questions = state_data["mode_questions"]
        # example -> eng

        try:
            search_para = data_base.select_data_(method_1=method_add_data,
                                                 method_2=mode_questions, where_data=answer, output_para="on")

            del_msg = await bot.send_message(message.from_user.id, f"Обратите внимание, "
                                                                   f"найдены совпадения: "
                                                                   f"{message_(search_para, word_=answer)}")
            list_delete.append(del_msg.message_id)

        except Exception as ex:
            logger_(message.from_user.id, f"file: handlers/add_word_quit_2 /// {ex}")

        list_delete.append(message.message_id)

        keyboard_cancel = Keyboard(["Отмена ->"])

        match state_data["mode_questions"]:

            case "rus":
                await state.update_data(rus_add_data=answer)

                del_msg = await bot.send_message(message.from_user.id,
                                                 f"{handlers_dict[f'add_{method_add_data}_last']}",
                                                 reply_markup=keyboard_cancel.create_keyboard(3))
                list_delete.append(del_msg.message_id)

                await state.update_data(list_delete=list_delete)
                await QuestionParams.add_word_last.set()

            case "eng":
                await state.update_data(eng_add_data=answer)

                del_msg = await bot.send_message(message.from_user.id,
                                                 f"{handlers_dict[f'add_{method_add_data}_first']}",
                                                 reply_markup=keyboard_cancel.create_keyboard(3))
                list_delete.append(del_msg.message_id)

                await state.update_data(list_delete=list_delete)
                await QuestionParams.add_word_last.set()


async def add_word_last(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    answer = message.text

    if answer == "Отмена ->":
        await bot.delete_message(message.chat.id, message.message_id)

        keyboard_start = Keyboard(buttons_main_menu)

        await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                               reply_markup=keyboard_start.create_keyboard(3))

        finally_state_data = await state.get_data()

        await delete_message(message.chat.id, finally_state_data["list_delete"])

        await state.finish()

    else:
        state_data = await state.get_data()

        list_delete = state_data["list_delete"]

        match state_data["mode_questions"]:
            case "rus":
                await state.update_data(eng_add_data=answer)
            case "eng":
                await state.update_data(rus_add_data=answer)

        state_data_ = await state.get_data()
        list_delete.append(message.message_id)

        rus_add_data = state_data_["rus_add_data"]
        eng_add_data = state_data_["eng_add_data"]
        method_add_data = state_data_["method_add_data"]
        mode_add_word = state_data_["mode_add_word"]

        data_base = db2.DB(message.from_user.id)
        data_base.insert_word_phrase(method_add_data, rus_add_data, eng_add_data)

        if mode_add_word == "ask":
            keyboard_quit = Keyboard(["Нет", "Да"])

            del_mag = await bot.send_message(message.from_user.id, f"Пара {rus_add_data} - {eng_add_data} "
                                                                   f"была добавлена\n"
                                                                   f"{handlers_dict[f'add_{method_add_data}_quit']}",
                                             reply_markup=keyboard_quit.create_keyboard(3))
            list_delete.append(del_mag.message_id)

            await state.update_data(list_delete=list_delete)
            await QuestionParams.add_word_quit.set()

        elif mode_add_word == "auto":
            try:
                del_msg = state_data["add_word_quit_await"]
                list_delete.append(del_msg.message_id)
            except Exception as ex:
                logger_(message.from_user.id, f"file: handlers/add_word_quit_2 /// {ex}")

            state_data = await state.get_data()

            keyboard_cancel = Keyboard(["Готово ->"])

            match state_data["mode_questions"]:
                case "rus":
                    await state.update_data(rus_add_data=answer)

                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"""
                                                     {handlers_dict[f'add_{state_data["method_add_data"]}_first']}""",
                                                     reply_markup=keyboard_cancel.create_keyboard(3))
                    list_delete.append(del_msg.message_id)

                    await state.update_data(list_delete=list_delete)
                    await QuestionParams.add_word_last.set()

                case "eng":
                    await state.update_data(eng_add_data=answer)

                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"""
                                                     {handlers_dict[f'add_{state_data["method_add_data"]}_last']}""",
                                                     reply_markup=keyboard_cancel.create_keyboard(3))
                    list_delete.append(del_msg.message_id)

            await state.update_data(list_delete=list_delete)
            await QuestionParams.add_word_first.set()


async def add_word_quit(message: types.Message, state: FSMContext):
    """ Спрашиваем за повторный ввод данных, есл нет - переводим на главное меню """

    state_data = await state.get_data()
    list_delete = state_data["list_delete"]

    answer = message.text
    list_delete.append(message.message_id)

    match answer:
        case "Нет":
            try:
                add_word_quit_await = state_data["add_word_quit_await"]

                list_delete.append(add_word_quit_await.message_id)
                await state.update_data(list_delete=list_delete)

            except Exception as ex:
                logger_(message.from_user.id, f"file: handlers/add_word_quit_1 /// {ex}")

            await state.update_data(list_delete=list_delete)

            keyboard_start = Keyboard(buttons_main_menu)

            await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                   reply_markup=keyboard_start.create_keyboard(3))

            finally_state_data = await state.get_data()

            await delete_message(message.chat.id, finally_state_data["list_delete"])

            await state.finish()

        case "Да":
            try:
                del_msg = state_data["add_word_quit_await"]
                list_delete.append(del_msg.message_id)
            except Exception as ex:
                logger_(message.from_user.id, f"file: handlers/add_word_quit_2 /// {ex}")

            state_data = await state.get_data()

            keyboard_cancel = Keyboard(["Отмена ->"])

            match state_data["mode_questions"]:
                case "rus":
                    await state.update_data(rus_add_data=answer)

                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"""
                                                     {handlers_dict[f'add_{state_data["method_add_data"]}_first']}""",
                                                     reply_markup=keyboard_cancel.create_keyboard(3))
                    list_delete.append(del_msg.message_id)

                    await state.update_data(list_delete=list_delete)
                    await QuestionParams.add_word_last.set()

                case "eng":
                    await state.update_data(eng_add_data=answer)

                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"""
                                                     {handlers_dict[f'add_{state_data["method_add_data"]}_last']}""",
                                                     reply_markup=keyboard_cancel.create_keyboard(3))
                    list_delete.append(del_msg.message_id)

            await state.update_data(list_delete=list_delete)
            await QuestionParams.add_word_first.set()


async def start_test(message: types.Message, state: FSMContext):
    """ Начало машины состояния """

    data_base = db2.DB(message.from_user.id)

    answer = message.text

    len_data = []
    message_print = ""
    try:
        match answer:
            case "Пройти тест: слова ->":
                len_data = len(data_base.select_data_(column_="word_rus", all_="on"))
                message_print = "слов"

            case "Пройти тест: фразы ->":
                len_data = len(data_base.select_data_(column_="phrase_rus", all_="on"))
                message_print = "фраз"
    except Exception as ex:
        logger_(message.from_user.id, f"file: handlers/start_test /// {ex}")

    if len_data < 10:
        await bot.send_message(message.from_user.id, f"Минимальное значение {message_print} для начала теста - 10.\n"
                                                     f"На данный момент у вас {message_print} - {len_data} ")
        await bot.delete_message(message.chat.id, message.message_id)

    else:
        await state.update_data(param_questions=int(json.loads(data_base.select_data_(
                                column_="params_user")[0][0])["param_questions"]))

        await state.update_data(param_percent=int(json.loads(data_base.select_data_(
                                column_="params_user", where_clmn="id", where_data=1)[0][0])["param_percent"]))

        await state.update_data(len_data=len_data)

        await state.update_data(count_fails=0)
        await state.update_data(count_questions=0)
        await state.update_data(status_=0)
        await state.update_data(temp_method=answer)
        await state.update_data(list_fails=[])
        await state.update_data(list_asked_data=[])

        await bot.delete_message(message.chat.id, message.message_id)

        keyboard_start_test = Keyboard(["Назад ->", "Начать ->"])

        del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict[f'start_test_word_1']}",
                                         reply_markup=keyboard_start_test.create_keyboard(3))

        del_msg_2 = await bot.send_message(message.from_user.id, f"{handlers_dict[f'start_test_word_2']}",
                                           reply_markup=keyboard_choose(message.from_user.id))

        await state.update_data(list_delete=[message.message_id, del_msg.message_id, del_msg_2.message_id])


async def question_test(message: types.Message, state: FSMContext):
    """ Here we are sorting words by user-specified timeframe and word display options
         1 - Last week, 2 - All time, 3 - Russian --> English, 4 - English --> Russian """

    state_data = await state.get_data()

    answer = message.text

    if answer == "Назад ->" or answer == "Начать ->":
        await bot.delete_message(message.chat.id, message.message_id)

    try:
        list_delete = state_data["list_delete"]
        list_delete.append(message.message_id)
        await state.update_data(list_delete=list_delete)

    except Exception as ex:
        logger_(message.from_user.id, f"file: handlers/question_test_1 /// {ex}")

    param_questions = int(state_data["param_questions"])
    param_percent = int(state_data["param_percent"])
    count_fails = int(state_data["count_fails"])
    count_questions = int(state_data["count_questions"])
    status_ = int(state_data["status_"])

    temp_method = state_data["temp_method"]
    list_asked_data = state_data["list_asked_data"]
    len_data = state_data["len_data"]

    match answer:
        case "Назад ->":
            count_questions = param_questions

        case _:
            match status_:
                case 0:
                    pass

                case 1:
                    list_fails = state_data["list_fails"]

                    if count_questions < param_questions:
                        if str(answer.lower()) == str(state_data["answer_state"].lower()):
                            pass

                        elif str(answer.lower()) != str(state_data["answer_state"].lower()):

                            count_fails += 1
                            await state.update_data(count_fails=count_fails)
                            list_fails_ = [state_data["origin_para"], answer]
                            list_fails.append(list_fails_)

                            await state.update_data(list_fails=list_fails)

                    else:
                        if str(answer.lower()) == str(state_data["answer_state"].lower()):
                            pass

                        elif str(answer.lower()) != str(state_data["answer_state"].lower()):

                            count_fails += 1
                            await state.update_data(count_fails=count_fails)

                            list_fails_ = [state_data["origin_para"], answer]
                            list_fails.append(list_fails_)
                            await state.update_data(list_fails=list_fails)

                        max_percent_fails = 100 - param_percent
                        # Calculate the minimum % to determine if you pass the test.
                        # Example: 100 - 70 - 30 % available for errors

                        actual_percent = (count_fails / param_questions) * 100
                        # Example 3/10 * 100 = 30%

                        if count_fails == 0:
                            await bot.send_message(message.from_user.id,
                                                   f"Тест пройден. Ваш процент ответов - 100%")

                        else:
                            if actual_percent > max_percent_fails:
                                list_fails = state_data["list_fails"]

                                await bot.send_message(message.from_user.id,
                                                       f"Тест НЕ пройден. Ваш процент ответов - "
                                                       f"{str(100 - int(actual_percent))[0:5]}% "
                                                       f"из требуемых {param_percent}%")

                                await bot.send_message(message.from_user.id,
                                                       f"Слова в которых допускались ошибки: "
                                                       f"{message_(list_fails)}")

                            elif actual_percent <= max_percent_fails:
                                await bot.send_message(message.from_user.id,
                                                       f"Тест пройден. Ваш процент ответов - "
                                                       f"{str(100 - int(actual_percent))[0:5]}% "
                                                       f"из требуемых {param_percent}%")

                                await bot.send_message(message.from_user.id,
                                                       f"Слова в которых допускались ошибки: "
                                                       f"{message_(list_fails)}")

    # Output to the main menu after the last question
    if count_questions == param_questions:

        match answer:
            case "Назад ->":

                keyboard_start = Keyboard(buttons_main_menu)

                await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                       reply_markup=keyboard_start.create_keyboard(3))

                finally_state_data = await state.get_data()

                await delete_message(message.chat.id, finally_state_data["list_delete"])

                await state.finish()

            case _:

                keyboard_start = Keyboard(buttons_main_menu)

                await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                       reply_markup=keyboard_start.create_keyboard(3))

                finally_state_data = await state.get_data()

                if finally_state_data != 0:
                    await delete_message(message.chat.id, finally_state_data["list_delete"])
                else:
                    pass

                await state.finish()

    else:
        list_delete = state_data["list_delete"]
        match temp_method:
            case "Пройти тест: слова ->":

                data_ = check_word_phrase_replay("word", message.from_user.id, list_asked_data, len_data)

                list_asked_data.append(data_[1][0])
                await state.update_data(list_asked_data=list_asked_data)

                match data_:
                    case None:
                        del_msg = await bot.send_message(message.from_user.id, f"Вы не указали один из параметров ")
                        list_delete.append(del_msg.message_id)

                    case _:
                        match data_[0]:
                            case int(3):
                                # "3": "rus --> eng "
                                del_msg = await bot.send_message(message.from_user.id,
                                                                 f"Как переводится слово {data_[1][0]}",
                                                                 reply_markup=types.ReplyKeyboardRemove())
                                list_delete.append(del_msg.message_id)

                                await state.update_data(origin_para=data_[1])
                                await state.update_data(question_state=data_[1][0])
                                await state.update_data(answer_state=data_[1][1])

                                count_questions += 1
                                await state.update_data(count_questions=count_questions)

                                status_ = 1
                                await state.update_data(status_=status_)
                                await QuestionParams.question_test.set()

                            case int(4):
                                # "4": "eng --> rus "
                                del_msg = await bot.send_message(message.from_user.id,
                                                                 f"Как переводится слово {data_[1][1]}",
                                                                 reply_markup=types.ReplyKeyboardRemove())
                                list_delete.append(del_msg.message_id)

                                await state.update_data(origin_para=data_[1])
                                await state.update_data(question_state=data_[1][1])
                                await state.update_data(answer_state=data_[1][0])

                                count_questions += 1
                                await state.update_data(count_questions=count_questions)

                                status_ = 1
                                await state.update_data(status_=status_)
                                await QuestionParams.question_test.set()

            case "Пройти тест: фразы ->":

                data_ = check_word_phrase_replay("phrase", message.from_user.id, list_asked_data, len_data)

                list_asked_data.append(data_[1][0])
                await state.update_data(list_asked_data=list_asked_data)

                match data_[0]:
                    case int(3):
                        # "3": "rus --> eng "
                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"Как переводится фраза {data_[1][0]}",
                                                         reply_markup=types.ReplyKeyboardRemove())
                        list_delete.append(del_msg.message_id)

                        await state.update_data(origin_para=data_[1])
                        await state.update_data(question_state=data_[1][0])
                        await state.update_data(answer_state=data_[1][1])

                        count_questions += 1
                        await state.update_data(count_questions=count_questions)

                        status_ = 1
                        await state.update_data(status_=status_)
                        await QuestionParams.question_test.set()

                    case int(4):
                        # "4": "eng --> rus "
                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"Как переводится фраза {data_[1][1]}",
                                                         reply_markup=types.ReplyKeyboardRemove())
                        list_delete.append(del_msg.message_id)

                        await state.update_data(origin_para=data_[1])
                        await state.update_data(question_state=data_[1][1])
                        await state.update_data(answer_state=data_[1][0])

                        count_questions += 1
                        await state.update_data(count_questions=count_questions)

                        status_ = 1
                        await state.update_data(status_=status_)
                        await QuestionParams.question_test.set()

        await state.update_data(list_delete=list_delete)


async def user_settings(message: types.Message, state: FSMContext):
    """ Write down the second word and ask if the second word is to be written """

    await bot.delete_message(message.chat.id, message.message_id)

    data_base = db2.DB(message.from_user.id)

    await state.update_data(user_settings_status=0)

    keyboard_settings = Keyboard(buttons_settings_menu)

    len_dict_word = 0
    len_dict_phrase = 0

    try:
        len_dict_word = len(data_base.select_data_(column_=None))

        # len_dict_word = len(data_base.select_data_(column_="word_rus", all_="on"))
        len_dict_phrase = len(data_base.select_data_(column_="phrase_rus", all_="on"))
    except Exception as ex:
        logger_(message.from_user.id, f"file: handlers/user_settings /// {ex}")

    params_user = json.loads(data_base.select_data_(
        column_="params_user", where_clmn="id", where_data=1)[0][0])

    mode_questions = params_user["mode_questions"]

    match mode_questions:
        case "rus":
            mode_questions = "rus --> Eng"
        case "eng":
            mode_questions = "Eng --> rus"

    mode_add_word = params_user["mode_add_word"]
    match mode_add_word:
        case "ask":
            mode_add_word = "Ручной"
        case "auto":
            mode_add_word = "Автоматический"

    del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict[f'user_settings']}\n\n"
                                                           f"Количество вопросов: "
                                                           f"{params_user['param_questions']}\n"
                                                           f"Процент ошибок: "
                                                           f"{params_user['param_percent']}%\n"
                                                           f"Ручной период для теста: "
                                                           f"{params_user['param_day']} дней\n"
                                                           f"Порядок добавления слов: {mode_questions}\n"
                                                           f"Режим добавления слов: {mode_add_word}\n\n"
                                                           f"Всего слов добавлено: {len_dict_word}\n"
                                                           f"Всего фраз добавлено: {len_dict_phrase}\n",
                                     reply_markup=keyboard_settings.create_keyboard(4))

    await state.update_data(list_delete_usr_set_upd=[del_msg.message_id])
    await QuestionParams.user_settings_update.set()


async def user_settings_update(message: types.Message, state: FSMContext):
    """ Write down the second word and ask if the second word is to be written """

    answer = message.text

    data_base = db2.DB(message.from_user.id)

    params_user = json.loads(data_base.select_data_(
        column_="params_user", where_clmn="id", where_data=1)[0][0])

    state_data = await state.get_data()

    list_delete_usr_set_upd = state_data["list_delete_usr_set_upd"]
    list_delete_usr_set_upd.append(message.message_id)

    try:
        user_settings_status = int(state_data["user_settings_status"])
    except Exception as ex:
        logger_(message.from_user.id, f"file: handlers/user_settings_update_1 /// {ex}")
        user_settings_status = 0

    match user_settings_status:
        case 0:

            if answer == buttons_settings_menu[-1]:
                keyboard_start = Keyboard(buttons_main_menu)

                await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                       reply_markup=keyboard_start.create_keyboard(3))

                finally_state_data = await state.get_data()

                await delete_message(message.chat.id, finally_state_data["list_delete_usr_set_upd"])

                await bot.delete_message(message.chat.id, message.message_id)
                await state.finish()

            elif answer == buttons_settings_menu[0]:
                del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_q']}")
                list_delete_usr_set_upd.append(del_msg.message_id)

                await state.update_data(user_settings_status=1)
                await state.update_data(user_settings_update=answer)
                await QuestionParams.user_settings_update.set()

            elif answer == buttons_settings_menu[1]:
                del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_%']}")
                list_delete_usr_set_upd.append(del_msg.message_id)

                await state.update_data(user_settings_status=1)
                await state.update_data(user_settings_update=answer)
                await QuestionParams.user_settings_update.set()

            elif answer == buttons_settings_menu[2]:
                del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_d']}")
                list_delete_usr_set_upd.append(del_msg.message_id)

                await state.update_data(user_settings_status=1)
                await state.update_data(user_settings_update=answer)
                await QuestionParams.user_settings_update.set()

            elif answer == buttons_settings_menu[3]:
                keyboard_answer = Keyboard(["rus ->", "Eng ->"])

                del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_a']}",
                                                 reply_markup=keyboard_answer.create_keyboard(3))
                list_delete_usr_set_upd.append(del_msg.message_id)

                await state.update_data(user_settings_status=1)
                await state.update_data(user_settings_update=answer)
                await QuestionParams.user_settings_update.set()

            elif answer == buttons_settings_menu[4]:
                keyboard_answer = Keyboard(["Ручной ->", "Авто ->"])

                del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_m']}",
                                                 reply_markup=keyboard_answer.create_keyboard(3))
                list_delete_usr_set_upd.append(del_msg.message_id)

                await state.update_data(user_settings_status=1)
                await state.update_data(user_settings_update=answer)
                await QuestionParams.user_settings_update.set()

            elif answer == buttons_settings_menu[5]:
                try:
                    random_question("word", message.from_user.id, mode_func="download")

                # doc = open(f'/Users/macbook/Desktop/english_bot_test/temporary/words_id_{message.from_user.id}.txt')
                    doc = open(f'/home/ubuntu/eng_bot/temporary/words_id_{message.from_user.id}.txt')
                    await bot.send_document(message.from_user.id, doc)
                    await bot.delete_message(message.chat.id, message.message_id)

                except Exception as ex:
                    del_msg = await bot.send_message(message.from_user.id, f"У Вас нет слов для скачивания ")
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    logger_(message.from_user.id, f"file: handlers/user_settings_update_2 /// {ex}")

            elif answer == buttons_settings_menu[6]:
                try:
                    random_question("phrase", message.from_user.id, mode_func="download")
                # doc = open(f'/Users/macbook/Desktop/english_bot_test/temporary/words_id_{message.from_user.id}.txt')
                    doc = open(f'/home/ubuntu/eng_bot/temporary/words_id_{message.from_user.id}.txt')
                    await bot.send_document(message.from_user.id, doc)
                    await bot.delete_message(message.chat.id, message.message_id)

                except Exception as ex:
                    del_msg = await bot.send_message(message.from_user.id, f"У Вас нет фраз для скачивания ")
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    logger_(message.from_user.id, f"file: handlers/user_settings_update_3 /// {ex}")

            else:
                del_msg = await bot.send_message(message.from_user.id, f"Выберите одну из опций ниже ⬇️⬇️⬇️")
                list_delete_usr_set_upd.append(del_msg.message_id)

            await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)

        case 1:
            try:
                if state_data["user_settings_update"] == buttons_settings_menu[0]:
                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"{handlers_dict['user_settings_update_accept_q']} - {answer}")
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    params_user["param_questions"] = int(answer)

                    await state.update_data(user_settings_status=0)
                    user_settings_status = 1

                elif state_data["user_settings_update"] == buttons_settings_menu[1]:
                    if int(answer) > 100:
                        del_msg = await bot.send_message(message.from_user.id, f"Вводите число от 0 до 100")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        await state.update_data(user_settings_status=0)
                        user_settings_status = 1

                    else:

                        params_user["param_percent"] = int(answer)

                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"{handlers_dict['user_settings_update_accept_%']} - "
                                                         f"{answer}%")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        await state.update_data(user_settings_status=0)
                        user_settings_status = 1

                elif state_data["user_settings_update"] == buttons_settings_menu[2]:
                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"{handlers_dict['user_settings_update_accept_d']} - {answer}")
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    params_user["param_day"] = int(answer)

                    await state.update_data(user_settings_status=0)
                    user_settings_status = 1

                elif state_data["user_settings_update"] == buttons_settings_menu[3] or \
                        state_data["user_settings_update"] == buttons_settings_menu[4]:

                    keyboard_settings = Keyboard(buttons_settings_menu)

                    if answer == "rus ->" or answer == "Eng ->":

                        if answer == "rus ->":
                            params_user["mode_questions"] = "rus"

                        elif answer == "Eng ->":
                            params_user["mode_questions"] = "eng"

                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"{handlers_dict['user_settings_update_accept_a']}"
                                                         f" - {answer}",
                                                         reply_markup=keyboard_settings.create_keyboard(4))
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        await state.update_data(user_settings_status=0)
                        user_settings_status = 1

                    elif answer == "Ручной ->" or answer == "Авто ->":

                        if answer == "Ручной ->":
                            params_user["mode_add_word"] = "ask"

                        elif answer == "Авто ->":
                            params_user["mode_add_word"] = "auto"

                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"{handlers_dict['user_settings_update_accept_m']}"
                                                         f" - {answer}",
                                                         reply_markup=keyboard_settings.create_keyboard(4))
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        await state.update_data(user_settings_status=0)
                        user_settings_status = 1

                    else:
                        del_msg = await bot.send_message(message.from_user.id, f"Используйте кнопки",
                                                         reply_markup=keyboard_settings.create_keyboard(4))
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        await state.update_data(user_settings_status=0)
                        user_settings_status = 1

            except Exception as ex:
                user_settings_status = 1
                logger_(message.from_user.id, f"file: handlers/user_settings_update_4 /// {ex}")

            data_base.update_data_(column_="params_user", data_updating=json.dumps(params_user))
            await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)

    if user_settings_status == 1:
        await QuestionParams.user_settings_update.set()
        await bot.delete_message(message.chat.id, message.message_id)

        await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)


async def replay_questions(message: types.Message):
    """ Начало машины состояния """

    data_base = db2.DB(message.from_user.id)

    word_rus = len(data_base.select_data_(column_="word_rus", all_="on"))

    if word_rus < 10:
        await bot.send_message(message.from_user.id, f"Минимальное значение слов для повторения - 10.\n"
                                                     f"На данный момент у вас слов - {word_rus} ")
        await bot.delete_message(message.chat.id, message.message_id)

    else:
        await bot.delete_message(message.chat.id, message.message_id)

        del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict[f'replay_word']}",
                                         reply_markup=keyboard_choose_replay("word", message.from_user.id))

        data_base.update_data_(column_="temp_data", where_data=2, data_updating=del_msg.message_id)
        data_base.update_data_(column_="temp_data", where_data=5, data_updating=0)


async def delete_message(user_id, list_message):
    for del_msg in list_message:
        try:
            await bot.delete_message(user_id, del_msg)
        except Exception as ex:
            logger_(user_id, f"file: handlers/delete_message /// {ex}")


def register_handler_command(dp: Dispatcher):
    dp.register_message_handler(add_word, Text(equals="Добавить слово ->"))
    dp.register_message_handler(add_word, Text(equals="Добавить фразу ->"))

    dp.register_message_handler(start_test, Text(equals="Пройти тест: слова ->"))
    dp.register_message_handler(start_test, Text(equals="Пройти тест: фразы ->"))

    dp.register_message_handler(add_word_first, state=QuestionParams.add_word_first)
    dp.register_message_handler(add_word_last, state=QuestionParams.add_word_last)
    dp.register_message_handler(add_word_quit, state=QuestionParams.add_word_quit)

    dp.register_message_handler(question_test, Text(equals="Начать ->"))
    dp.register_message_handler(question_test, Text(equals="Назад ->"))

    dp.register_message_handler(user_settings, Text(equals="Настройки ->"))
    dp.register_message_handler(user_settings_update, state=QuestionParams.user_settings_update)

    dp.register_message_handler(question_test, state=QuestionParams.question_test)

    dp.register_message_handler(replay_questions, Text(equals="Повторение слова ->"))
