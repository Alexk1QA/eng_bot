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

    param_answer_ = "param_answer"
    data_base = db2.DB(message.from_user.id)

    param_answer = data_base.select_data(param_answer_)[0][0]

    await state.update_data(mode_ask=param_answer)

    await bot.delete_message(message.chat.id, message.message_id)

    answer = message.text

    match answer:
        case "Добавить слово ->":
            await state.update_data(method_add_data="word")

        case "Добавить фразу ->":
            await state.update_data(method_add_data="phrase")

    state_data = await state.get_data()
    method_add_data = state_data["method_add_data"]
    mode_ask = state_data["mode_ask"]

    button = ["Отмена ->"]
    keyboard_cancel = Keyboard(button)

    match mode_ask:
        case 0:
            del_msg = await bot.send_message(message.from_user.id,
                                             f"{handlers_dict[f'add_{method_add_data}_first']}",
                                             reply_markup=keyboard_cancel.create_keyboadr(3))

            await state.update_data(list_delete=[message.message_id, del_msg.message_id])
            await QuestionParams.add_word_first.set()

        case 1:
            del_msg = await bot.send_message(message.from_user.id,
                                             f"{handlers_dict[f'add_{method_add_data}_last']}",
                                             reply_markup=keyboard_cancel.create_keyboadr(3))

            await state.update_data(list_delete=[message.message_id, del_msg.message_id])
            await QuestionParams.add_word_first.set()


async def add_word_first(message: types.Message, state: FSMContext):
    """ Записываем первое слово или фразу и спрашиваем второе """

    answer = message.text

    if answer == "Отмена ->":
        await bot.delete_message(message.chat.id, message.message_id)

        button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                  "Пройти тест: фразы ->", "Повторение слова ->", "Настройки ->"]
        keyboard_start = Keyboard(button)
        await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                               reply_markup=keyboard_start.create_keyboadr(3))

        finally_state_data = await state.get_data()
        list_delete = finally_state_data["list_delete"]

        for del_msg in list_delete:
            try:
                await bot.delete_message(message.chat.id, del_msg)
            except Exception as ex:
                print(ex)
                pass

        await state.finish()

    else:
        state_data = await state.get_data()

        list_delete = state_data["list_delete"]
        method_add_data = state_data["method_add_data"]
        mode_ask = state_data["mode_ask"]

        list_delete.append(message.message_id)

        button = ["Отмена ->"]
        keyboard_cancel = Keyboard(button)

        match mode_ask:
            case 0:
                await state.update_data(rus_add_data=answer)

                del_msg = await bot.send_message(message.from_user.id,
                                                 f"{handlers_dict[f'add_{method_add_data}_last']}",
                                                 reply_markup=keyboard_cancel.create_keyboadr(3))
                list_delete.append(del_msg.message_id)

                await state.update_data(list_delete=list_delete)
                await QuestionParams.add_word_last.set()

            case 1:
                await state.update_data(eng_add_data=answer)

                del_msg = await bot.send_message(message.from_user.id,
                                                 f"{handlers_dict[f'add_{method_add_data}_first']}",
                                                 reply_markup=keyboard_cancel.create_keyboadr(3))
                list_delete.append(del_msg.message_id)

                await state.update_data(list_delete=list_delete)
                await QuestionParams.add_word_last.set()


async def add_word_last(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    answer = message.text

    if answer == "Отмена ->":
        await bot.delete_message(message.chat.id, message.message_id)

        button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                  "Пройти тест: фразы ->", "Повторение слова ->", "Настройки ->"]
        keyboard_start = Keyboard(button)
        await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                               reply_markup=keyboard_start.create_keyboadr(3))

        finally_state_data = await state.get_data()

        list_delete = finally_state_data["list_delete"]

        for del_msg in list_delete:
            try:
                await bot.delete_message(message.chat.id, del_msg)
            except Exception as ex:
                print(ex)
                pass

        await state.finish()

    else:
        state_data = await state.get_data()

        list_delete = state_data["list_delete"]
        mode_ask = state_data["mode_ask"]

        match mode_ask:
            case 0:
                await state.update_data(eng_add_data=answer)
            case 1:
                await state.update_data(rus_add_data=answer)

        state_data_ = await state.get_data()
        list_delete.append(message.message_id)

        rus_add_data = state_data_["rus_add_data"]
        eng_add_data = state_data_["eng_add_data"]
        method_add_data = state_data_["method_add_data"]

        create_table = db2.DB(message.from_user.id)
        create_table.insert_data(method_add_data, rus_add_data, eng_add_data)

        button = ["Нет", "Да"]
        keyboard_quit = Keyboard(button)

        del_mag = await bot.send_message(message.from_user.id, f"Пара {rus_add_data} - {eng_add_data} "
                                         f"была добавлена\n"
                                         f"{handlers_dict[f'add_{method_add_data}_quit']}",
                                         reply_markup=keyboard_quit.create_keyboadr(3))
        list_delete.append(del_mag.message_id)

        await state.update_data(list_delete=list_delete)
        await QuestionParams.add_word_quit.set()


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
                print(ex)
                pass

            await state.update_data(list_delete=list_delete)

            button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                      "Пройти тест: фразы ->", "Повторение слова ->", "Настройки ->"]
            keyboard_start = Keyboard(button)

            await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                   reply_markup=keyboard_start.create_keyboadr(3))

            finally_state_data = await state.get_data()

            list_delete = finally_state_data["list_delete"]

            for del_msg in list_delete:
                try:
                    await bot.delete_message(message.chat.id, del_msg)
                except Exception as ex:
                    print(ex)
                    pass

            await state.finish()

        case "Да":
            try:
                del_msg = state_data["add_word_quit_await"]
                list_delete.append(del_msg.message_id)
            except Exception as ex:
                print(ex)
                pass

            state_data = await state.get_data()
            method_add_data = state_data["method_add_data"]
            mode_ask = state_data["mode_ask"]

            button = ["Отмена ->"]
            keyboard_cancel = Keyboard(button)

            match mode_ask:
                case 0:
                    await state.update_data(rus_add_data=answer)

                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"{handlers_dict[f'add_{method_add_data}_first']}",
                                                     reply_markup=keyboard_cancel.create_keyboadr(3))
                    list_delete.append(del_msg.message_id)

                    await state.update_data(list_delete=list_delete)
                    await QuestionParams.add_word_last.set()

                case 1:
                    await state.update_data(eng_add_data=answer)

                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"{handlers_dict[f'add_{method_add_data}_last']}",
                                                     reply_markup=keyboard_cancel.create_keyboadr(3))
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
                len_data = len(data_base.select_data("word_rus"))
                message_print = "слов"

            case "Пройти тест: фразы ->":
                len_data = len(data_base.select_data("phrase_rus"))
                message_print = "фраз"
    except Exception as ex:
        print(ex)
        pass

    if len_data < 10:
        await bot.send_message(message.from_user.id, f"Минимальное значение {message_print} для начала теста - 10.\n"
                                                     f"На данный момент у вас {message_print} - {len_data} ")
        await bot.delete_message(message.chat.id, message.message_id)

    else:
        param_questions = "param_questions"
        param_percent = "param_percent"

        await state.update_data(param_questions=int(data_base.select_data(param_questions)[0][0]))
        await state.update_data(param_percent=int(data_base.select_data(param_percent)[0][0]))
        await state.update_data(count_fails=0)
        await state.update_data(count_questions=0)
        await state.update_data(status_=0)
        await state.update_data(temp_method=answer)
        await state.update_data(list_fails=[])

        button = ["Начать ->", "Назад ->"]

        keyboard_start_ = Keyboard(button)

        await bot.delete_message(message.chat.id, message.message_id)

        del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict[f'start_test_word_1']}",
                                         reply_markup=keyboard_start_.create_keyboadr(3))

        del_msg_2 = await bot.send_message(message.from_user.id, f"{handlers_dict[f'start_test_word_2']}",
                                           reply_markup=keyboard_choose(message.from_user.id))

        await state.update_data(list_delete=[message.message_id, del_msg.message_id, del_msg_2.message_id])


async def question_test(message: types.Message, state: FSMContext):
    """ Тут мы сортируем слова по сроку который указал пользователь и вариант отображения слов
         1 - За посл неделю, 2 - За все время, 3 - рус --> англ, 4 - англ --> рус """

    state_data = await state.get_data()

    answer = message.text

    if answer == "Назад ->" or answer == "Начать ->":
        await bot.delete_message(message.chat.id, message.message_id)

    try:
        list_delete = state_data["list_delete"]
        list_delete.append(message.message_id)
        await state.update_data(list_delete=list_delete)

    except Exception as ex:
        print(ex)
        pass

    param_questions = int(state_data["param_questions"])
    param_percent = int(state_data["param_percent"])
    count_fails = int(state_data["count_fails"])
    count_questions = int(state_data["count_questions"])
    status_ = int(state_data["status_"])

    temp_method = state_data["temp_method"]

    match answer:
        case "Назад ->":
            count_questions = param_questions

        case _:
            list_delete = state_data["list_delete"]
            match status_:
                case 0:
                    pass

                case 1:
                    origin_para = state_data["origin_para"]
                    answer_state = state_data["answer_state"]
                    list_fails = state_data["list_fails"]

                    if count_questions < param_questions:
                        if str(answer.lower()) == str(answer_state.lower()):
                            pass

                        elif str(answer.lower()) != str(answer_state.lower()):

                            count_fails += 1
                            await state.update_data(count_fails=count_fails)
                            list_fails_ = [origin_para, answer]
                            list_fails.append(list_fails_)

                            await state.update_data(list_fails=list_fails)

                    else:
                        if str(answer.lower()) == str(answer_state.lower()):
                            pass

                        elif str(answer.lower()) != str(answer_state.lower()):

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

                            del_msg = await bot.send_message(message.from_user.id,
                                                             f"Тест пройден. Ваш процент ответов - 100%")
                            list_delete.append(del_msg.message_id)

                        else:
                            finally_state_data = await state.get_data()

                            list_delete = finally_state_data["list_delete"]

                            for del_msg in list_delete:
                                try:
                                    await bot.delete_message(message.chat.id, del_msg)
                                except Exception as ex:
                                    print(ex)
                                    pass

                            if actual_percent > max_percent_fails:

                                list_fails = state_data["list_fails"]

                                del_msg = await bot.send_message(message.from_user.id,
                                                                 f"Тест НЕ пройден. Ваш процент ответов - "
                                                                 f"{str(100 - int(actual_percent))[0:5]}%")
                                list_delete.append(del_msg.message_id)

                                del_msg_2 = await bot.send_message(message.from_user.id,
                                                                   f"Слова в которых допускались ошибки: "
                                                                   f"{message_(list_fails)}")
                                list_delete.append(del_msg_2.message_id)

                            elif actual_percent <= max_percent_fails:
                                del_msg = await bot.send_message(message.from_user.id,
                                                                 f"Тест пройден. Ваш процент ответов - "
                                                                 f"{str(100 - int(actual_percent))[0:5]}%")
                                list_delete.append(del_msg.message_id)

                                del_msg_2 = await bot.send_message(message.from_user.id,
                                                                   f"Слова в которых допускались ошибки: "
                                                                   f"{message_(list_fails)}")
                                list_delete.append(del_msg_2.message_id)

    # Вывод на главное меню после последнего вопроса
    if count_questions == param_questions:

        match answer:
            case "Назад ->":
                button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                          "Пройти тест: фразы ->", "Повторение слова ->", "Настройки ->"]
                keyboard_start = Keyboard(button)
                await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                       reply_markup=keyboard_start.create_keyboadr(3))

                finally_state_data = await state.get_data()

                list_delete = finally_state_data["list_delete"]

                for del_msg in list_delete:
                    try:
                        await bot.delete_message(message.chat.id, del_msg)
                    except Exception as ex:
                        print(ex)
                        pass

                await state.finish()

            case _:
                button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                          "Пройти тест: фразы ->", "Повторение слова ->", "Настройки ->"]
                keyboard_start = Keyboard(button)
                await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                       reply_markup=keyboard_start.create_keyboadr(3))

                finally_state_data = await state.get_data()

                list_delete = finally_state_data["list_delete"]

                for del_msg in list_delete:
                    try:
                        await bot.delete_message(message.chat.id, del_msg)
                    except Exception as ex:
                        print(ex)
                        pass

                await state.finish()

    else:
        list_delete = state_data["list_delete"]
        match temp_method:
            case "Пройти тест: слова ->":
                data_ = random_question("word", message.from_user.id, 0)
                # example data_ --> # [3, ['Яблоко', 'Apple']]

                match data_[0]:
                    case int(3):
                        # "3": "рус --> англ "
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
                        # "4": "англ --> рус "
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
                data_ = random_question("phrase", message.from_user.id, 0)

                match data_[0]:
                    case int(3):
                        # "3": "рус --> англ "
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
                        # "4": "англ --> рус "
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
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    await bot.delete_message(message.chat.id, message.message_id)

    data_base = db2.DB(message.from_user.id)

    param_questions_ = "param_questions"
    param_percent_ = "param_percent"
    param_day = "param_day"

    await state.update_data(user_settings_status=0)
    await state.update_data(list_delete_usr_set_upd=[])

    buttons = ["Вопросы ->", "Процент ошибок ->", "Ручной режим ->", "Добавление слов ->",
               "Скачать слова ->", "Скачать фразы ->", "Назад ->"]

    keyboard_settings = Keyboard(buttons)

    len_dict_word = 0
    len_dict_phrase = 0

    try:
        len_dict_word = len(data_base.select_data("word_rus"))
        len_dict_phrase = len(data_base.select_data("phrase_rus"))
    except Exception as ex:
        print(ex)
        pass

    param_answer_ = "param_answer"
    param_answer = data_base.select_data(param_answer_)[0][0]

    match param_answer:
        case 0:
            param_answer = "rus --> Eng"
        case 1:
            param_answer = "Eng --> rus"

    await bot.send_message(message.from_user.id, f"{handlers_dict[f'user_settings']}\n\n"
                                                 f"Количество вопросов: "
                                                 f"{data_base.select_data(param_questions_)[0][0]}\n"
                                                 f"Процент ошибок: {data_base.select_data(param_percent_)[0][0]}%\n"
                                                 f"Ручной период для теста: "
                                                 f"{data_base.select_data(param_day)[0][0]} дней\n"
                                                 f"Порядок добавления слов: {param_answer}\n\n"
                                                 f"Всего слов добавлено: {len_dict_word}\n"
                                                 f"Всего фраз добавлено: {len_dict_phrase}\n",
                           reply_markup=keyboard_settings.create_keyboadr(4))

    await QuestionParams.user_settings_update.set()


async def user_settings_update(message: types.Message, state: FSMContext):
    """ Записываем второе слово и спрашиваем будет ли второе слово для записи """

    answer = message.text

    data_base = db2.DB(message.from_user.id)

    state_data = await state.get_data()

    list_delete_usr_set_upd = state_data["list_delete_usr_set_upd"]
    list_delete_usr_set_upd.append(message.message_id)

    try:
        user_settings_status = int(state_data["user_settings_status"])
    except Exception as ex:
        print(ex)

        user_settings_status = 0

    match user_settings_status:
        case 0:
            match answer:

                case "Назад ->":
                    button = ["Добавить слово ->", "Добавить фразу ->", "Пройти тест: слова ->",
                              "Пройти тест: фразы ->", "Повторение слова ->", "Настройки ->"]
                    keyboard_start = Keyboard(button)

                    await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                           reply_markup=keyboard_start.create_keyboadr(3))

                    finally_state_data = await state.get_data()

                    list_delete_usr_set_upd = finally_state_data["list_delete_usr_set_upd"]

                    for del_msg in list_delete_usr_set_upd:
                        try:
                            await bot.delete_message(message.chat.id, del_msg)
                        except Exception as ex:
                            print(ex)
                            pass

                    await bot.delete_message(message.chat.id, message.message_id)
                    await state.finish()

                case "Вопросы ->":
                    del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_q']}")
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    await state.update_data(user_settings_status=1)
                    await state.update_data(user_settings_update=answer)
                    await QuestionParams.user_settings_update.set()

                case "Процент ошибок ->":
                    del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_%']}")
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    await state.update_data(user_settings_status=1)
                    await state.update_data(user_settings_update=answer)
                    await QuestionParams.user_settings_update.set()

                case "Ручной режим ->":
                    del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_d']}")
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    await state.update_data(user_settings_status=1)
                    await state.update_data(user_settings_update=answer)
                    await QuestionParams.user_settings_update.set()

                case "Добавление слов ->":

                    button = ["rus ->", "Eng ->"]
                    keyboard_answer = Keyboard(button)

                    del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict['user_settings_update_a']}",
                                                     reply_markup=keyboard_answer.create_keyboadr(3))
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    await state.update_data(user_settings_status=1)
                    await state.update_data(user_settings_update=answer)
                    await QuestionParams.user_settings_update.set()

                case "Скачать слова ->":
                    try:
                        method_ = "word"
                        random_question(method_, message.from_user.id, 1)
                    # doc = open(f'/Users/macbook/Desktop/english_bot/temporary/words_id_{message.from_user.id}.txt')
                        doc = open(f'/home/ubuntu/eng_bot/temporary/words_id_{message.from_user.id}.txt')
                        await bot.send_document(message.from_user.id, doc)
                        await bot.delete_message(message.chat.id, message.message_id)

                    except Exception as ex:
                        print(ex)
                        del_msg = await bot.send_message(message.from_user.id, f"У Вас нет слов для скачивания ")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                case "Скачать фразы ->":
                    try:
                        method_ = "phrase"
                        random_question(method_, message.from_user.id, 1)
                    # doc = open(f'/Users/macbook/Desktop/english_bot/temporary/words_id_{message.from_user.id}.txt')
                        doc = open(f'/home/ubuntu/eng_bot/temporary/words_id_{message.from_user.id}.txt')
                        await bot.send_document(message.from_user.id, doc)
                        await bot.delete_message(message.chat.id, message.message_id)

                    except Exception as ex:
                        print(ex)
                        del_msg = await bot.send_message(message.from_user.id, f"У Вас нет фраз для скачивания ")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                case _:
                    del_msg = await bot.send_message(message.from_user.id, f"Выберите одну из опций ниже ⬇️⬇️⬇️")
                    list_delete_usr_set_upd.append(del_msg.message_id)

            await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)

        case 1:
            try:
                user_settings_update = state_data["user_settings_update"]

                match user_settings_update:

                    case "Вопросы ->":
                        answer = int(answer)
                        param_questions = "param_questions"

                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"{handlers_dict['user_settings_update_accept_q']} - {answer}")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        data_base.settings_update(param_questions, answer)

                        await state.update_data(user_settings_status=0)
                        user_settings_status = 1

                    case "Процент ошибок ->":
                        answer = int(answer)
                        param_percent = "param_percent"

                        if int(answer) > 100:
                            del_msg = await bot.send_message(message.from_user.id, f"Вводите число от 0 до 100")
                            list_delete_usr_set_upd.append(del_msg.message_id)

                            await state.update_data(user_settings_status=0)
                            user_settings_status = 1

                        else:
                            data_base.settings_update(param_percent, answer)

                            del_msg = await bot.send_message(message.from_user.id,
                                                             f"{handlers_dict['user_settings_update_accept_%']} - "
                                                             f"{answer}%")
                            list_delete_usr_set_upd.append(del_msg.message_id)

                            await state.update_data(user_settings_status=0)
                            user_settings_status = 1

                    case "Ручной режим ->":
                        answer = int(answer)
                        param_day = "param_day"

                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"{handlers_dict['user_settings_update_accept_d']} - {answer}")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        data_base.settings_update(param_day, answer)

                        await state.update_data(user_settings_status=0)
                        user_settings_status = 1

                    case "Добавление слов ->":
                        param_answer = "param_answer"

                        if answer == "rus ->":
                            data_base.settings_update(param_answer, 0)

                        elif answer == "Eng ->":
                            data_base.settings_update(param_answer, 1)

                        buttons = ["Вопросы ->", "Процент ошибок ->", "Ручной режим ->", "Добавление слов ->",
                                   "Скачать слова ->", "Скачать фразы ->", "Назад ->"]

                        keyboard_settings = Keyboard(buttons)

                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"{handlers_dict['user_settings_update_accept_a']} - {answer}",
                                                         reply_markup=keyboard_settings.create_keyboadr(4))
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        await state.update_data(user_settings_status=0)
                        user_settings_status = 1

            except Exception as ex:
                print(ex)
                user_settings_status = 1

            await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)

    if user_settings_status == 1:

        await QuestionParams.user_settings_update.set()
        await bot.delete_message(message.chat.id, message.message_id)

        await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)


async def replay_questions(message: types.Message):
    """ Начало машины состояния """

    data_base = db2.DB(message.from_user.id)

    word_rus = "word_rus"
    word_rus = len(data_base.select_data(word_rus))

    if word_rus < 10:
        await bot.send_message(message.from_user.id, f"Минимальное значение слов для повторения - 10.\n"
                                                     f"На данный момент у вас слов - {word_rus} ")
        await bot.delete_message(message.chat.id, message.message_id)

    else:
        method_ = "word"

        await bot.delete_message(message.chat.id, message.message_id)

        await bot.send_message(message.from_user.id, f"replay_questions {handlers_dict[f'replay_word']}",
                               reply_markup=keyboard_choose_replay(method_, message.from_user.id))


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
