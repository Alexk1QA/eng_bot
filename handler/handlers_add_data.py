import time

from aiogram.dispatcher import FSMContext
from handler.handlers import *
from state.states import *


async def add_word(message: types.Message, state: FSMContext):
    """ Начинаем машину состояния и спрашиваем первое слово или фразу """

    await delete_message_main(message.from_user.id, [])

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
            del_msg_1 = await bot.send_message(message.from_user.id, f"Режим добавления слов: Ручной"
                                                                     f"Вы добавляете слова в группу : "
                                                                     f"{data_base.actual_group()}")

        case "auto":
            del_msg_1 = await bot.send_message(message.from_user.id, f"Режим добавления слов: Автоматический\n"
                                                                     f"Вы добавляете слова в группу : "
                                                                     f"{data_base.actual_group()}")

    match state_data["mode_questions"]:
        case "rus":
            del_msg_2 = await bot.send_message(message.from_user.id,
                                               f"""{handlers_dict[f'add_{state_data["method_add_data"]}_first']}""")

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

        del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                              reply_markup=keyboard_start.create_keyboard(3))

        await delete_message_main(message.from_user.id, [del_msg_main.message_id])

        finally_state_data = await state.get_data()

        await delete_message(message.chat.id, finally_state_data["list_delete"], call_func="add_word_first")

        await state.finish()

    else:
        state_data = await state.get_data()

        list_delete = state_data["list_delete"]

        method_add_data = state_data["method_add_data"]
        # example -> word
        mode_questions = state_data["mode_questions"]
        # example -> eng

        try:
            search_para = data_base.select_data_(method_1=method_add_data, method_2=mode_questions,
                                                 where_data=answer, output_para="on")

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

        del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                              reply_markup=keyboard_start.create_keyboard(3))

        await delete_message_main(message.from_user.id, [del_msg_main.message_id])

        finally_state_data = await state.get_data()

        await delete_message(message.chat.id, finally_state_data["list_delete"], call_func="add_word_last")

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

            del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                                  reply_markup=keyboard_start.create_keyboard(3))

            await delete_message_main(message.from_user.id, [del_msg_main.message_id])

            finally_state_data = await state.get_data()

            await delete_message(message.chat.id, finally_state_data["list_delete"], call_func="add_word_quit")

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


def register_handler_command_add_data(dp: Dispatcher):
    dp.register_message_handler(add_word, Text(equals="Добавить слово ->"))
    dp.register_message_handler(add_word, Text(equals="Добавить фразу ->"))

    dp.register_message_handler(add_word_first, state=QuestionParams.add_word_first)
    dp.register_message_handler(add_word_last, state=QuestionParams.add_word_last)
    dp.register_message_handler(add_word_quit, state=QuestionParams.add_word_quit)
