from aiogram.dispatcher import FSMContext
from message import message_handlers
from handler.handlers import *
from state.states import *


async def user_settings(message: types.Message, state: FSMContext):
    """ Write down the second word and ask if the second word is to be written """

    await bot.delete_message(message.chat.id, message.message_id)

    await delete_message_main(message.from_user.id, [])

    data_base = db2.DB(message.from_user.id)

    await state.update_data(user_settings_status=0)

    keyboard_settings = Keyboard(buttons_settings_menu)

    len_dict_word = 0
    len_dict_phrase = 0

    try:
        len_dict_word = len(data_base.select_data_(column_="word_rus", all_="on", start_func="on"))
        len_dict_phrase = len(data_base.select_data_(column_="phrase_rus", all_="on", start_func="on"))
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

    user_group_ = user_group(message.from_user.id, mode="read_only")["user_group"]

    msg = message_(user_group_[f"dict_{user_group_['status']}"], len_word_in_groups="on", user_id=message.from_user.id)

    del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict[f'user_settings']}\n\n"
                                                                f"Количество вопросов при тесте: "
                                                                f"{params_user['param_questions']}\n"
                                                                f"Процент ошибок для тестов (min): "
                                                                f"{params_user['param_percent']}%\n"
                                                                f"Ручной период для теста: "
                                                                f"{params_user['param_day']} дней\n"
                                                                f"Порядок добавления слов: {mode_questions}\n"
                                                                f"Режим добавления слов: {mode_add_word}\n\n"
                                                                f"Всего слов добавлено: {len_dict_word}\n"
                                                                f"Всего фраз добавлено: {len_dict_phrase}\n\n"
                                                                f"Слов в таких группах:{msg}\n"
                                                                f"Более подробную информацию, вы можете посмотреть в "
                                                                f"разделе /info\n",
                                          reply_markup=keyboard_settings.create_keyboard(4))

    await state.update_data(list_delete_usr_set_upd=[])
    await delete_message_main(message.from_user.id, [del_msg_main.message_id], mode="",
                              where_data_add=3)

    await QuestionParams.user_settings_update.set()


async def user_settings_update(message: types.Message, state: FSMContext):
    """ Write down the second word and ask if the second word is to be written """

    answer = message.text

    data_base = db2.DB(message.from_user.id)

    params_user = json.loads(data_base.select_data_(column_="params_user", where_clmn="id", where_data=1)[0][0])

    state_data = await state.get_data()

    list_delete_usr_set_upd = state_data["list_delete_usr_set_upd"]
    list_delete_usr_set_upd.append(message.message_id)

    try:
        user_settings_status = int(state_data["user_settings_status"])
    except Exception as ex:
        logger_(message.from_user.id, f"file: handlers/user_settings_update_1 /// {ex}")
        user_settings_status = 0

    if answer == "Отмена ->":
        await bot.delete_message(message.chat.id, message.message_id)

        keyboard_start = Keyboard(buttons_main_menu)

        del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                              reply_markup=keyboard_start.create_keyboard(3))

        await delete_message_main(message.from_user.id, [del_msg_main.message_id])

        finally_state_data = await state.get_data()

        await delete_message(message.chat.id, finally_state_data["list_delete_usr_set_upd"], call_func="add_word_last")

        await state.finish()

    else:
        match user_settings_status:
            case 0:

                if answer == buttons_settings_menu[-1]:
                    keyboard_start = Keyboard(buttons_main_menu)

                    del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                                          reply_markup=keyboard_start.create_keyboard(3))

                    await delete_message_main(message.from_user.id, [del_msg_main.message_id])

                    finally_state_data = await state.get_data()

                    await delete_message(message.chat.id, finally_state_data["list_delete_usr_set_upd"],
                                         call_func="user_settings_update")

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
                    keyboard_answer = Keyboard(["Добавить группу ->", "Изменить группу ->", "Удалить группу ->",
                                                "Отмена ->"])
                    user_group_ = user_group(message.from_user.id, mode="read_only")["user_group"]

                    msg = message_(user_group_[f"dict_{user_group_['status']}"])

                    del_msg = await bot.send_message(message.from_user.id,
                                                     f"Вот список Ваших групп : {msg}"
                                                     f"(Список обновится после повторного входа в раздел 'Группы')\n\n"
                                                     f"{handlers_dict['user_settings_update_g']}",
                                                     reply_markup=keyboard_answer.create_keyboard(3))
                    list_delete_usr_set_upd.append(del_msg.message_id)

                    await state.update_data(user_settings_status=1)

                    await state.update_data(user_settings_status_group=0)

                    await state.update_data(user_settings_update=answer)
                    await QuestionParams.user_settings_update.set()

                elif answer == buttons_settings_menu[6]:
                    try:
                        random_question("word", message.from_user.id, mode_func="download")

            # doc = open(f'/Users/macbook/Desktop/english_bot_test/temporary/words_id_{message.from_user.id}.txt')
                        doc = open(f'/home/ubuntu/eng_bot/temporary/words_id_{message.from_user.id}.txt')
                        del_msg = await bot.send_document(message.from_user.id, doc)
                        list_delete_usr_set_upd.append(del_msg.message_id)
                        await bot.delete_message(message.chat.id, message.message_id)

                    except Exception as ex:
                        del_msg = await bot.send_message(message.from_user.id, f"У Вас нет слов для скачивания ")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        logger_(message.from_user.id, f"file: handlers/user_settings_update_2 /// {ex}")

                elif answer == buttons_settings_menu[7]:
                    try:
                        random_question("phrase", message.from_user.id, mode_func="download")
            # doc = open(f'/Users/macbook/Desktop/english_bot_test/temporary/'f'words_id_{message.from_user.id}.txt')
                        doc = open(f'/home/ubuntu/eng_bot/temporary/words_id_{message.from_user.id}.txt')
                        del_msg = await bot.send_document(message.from_user.id, doc)
                        list_delete_usr_set_upd.append(del_msg.message_id)
                        await bot.delete_message(message.chat.id, message.message_id)

                    except Exception as ex:
                        del_msg = await bot.send_message(message.from_user.id, f"У Вас нет фраз для скачивания ")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        logger_(message.from_user.id, f"file: handlers/user_settings_update_3 /// {ex}")

                elif answer == "/info":

                    await bot.delete_message(message.chat.id, message.message_id)

                    await delete_message_main(message.from_user.id, [])

                    button = ["Главное меню"]
                    keyboard_info = Keyboard(button)

                    del_msg_main = await bot.send_message(message.from_user.id,
                                                          f"{message_handlers.handlers_dict['info']}",
                                                          reply_markup=keyboard_info.create_keyboard(3))

                    await delete_message_main(message.from_user.id, [del_msg_main.message_id], mode="",
                                              where_data_add=3)

                    await state.finish()

                else:
                    del_msg = await bot.send_message(message.from_user.id, f"Выберите одну из опций ниже ⬇️⬇️⬇️")
                    list_delete_usr_set_upd.append(del_msg.message_id)

                await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)

            case 1:

                except_ = 0
                except__ = 0
                try:
                    if state_data["user_settings_update"] == buttons_settings_menu[0]:
                        # Вопросы ->
                        if int(answer):
                            del_msg = await bot.send_message(message.from_user.id,
                                                             f"{handlers_dict['user_settings_update_accept_q']} - "
                                                             f"{answer}")
                            list_delete_usr_set_upd.append(del_msg.message_id)

                            params_user["param_questions"] = int(answer)

                    elif state_data["user_settings_update"] == buttons_settings_menu[1]:
                        # Процент ошибок ->
                        if int(answer) > 100:
                            except__ = 5
                            raise ValueError

                        else:
                            params_user["param_percent"] = int(answer)

                            del_msg = await bot.send_message(message.from_user.id,
                                                             f"{handlers_dict['user_settings_update_accept_%']} - "
                                                             f"{answer}%")
                            list_delete_usr_set_upd.append(del_msg.message_id)
                            raise ZeroDivisionError

                    elif state_data["user_settings_update"] == buttons_settings_menu[2]:
                        # Ручной режим ->
                        del_msg = await bot.send_message(message.from_user.id,
                                                         f"{handlers_dict['user_settings_update_accept_d']} - "
                                                         f"{answer}")
                        list_delete_usr_set_upd.append(del_msg.message_id)

                        params_user["param_day"] = int(answer)

                    elif state_data["user_settings_update"] == buttons_settings_menu[3] or \
                            state_data["user_settings_update"] == buttons_settings_menu[4]:
                        # 3 - Добавление слов -> // 4 - Авто доб. слв.->
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

                        else:
                            del_msg = await bot.send_message(message.from_user.id, f"Используйте кнопки",
                                                             reply_markup=keyboard_settings.create_keyboard(4))
                            list_delete_usr_set_upd.append(del_msg.message_id)

                    elif state_data["user_settings_update"] == "Группы ->":

                        if state_data["user_settings_status_group"] == 0:
                            await state.update_data(user_settings_button_update=answer)

                        state_data = await state.get_data()

                        if state_data["user_settings_button_update"] == "Добавить группу ->":

                            if state_data["user_settings_status_group"] == 1:
                                pass
                            else:
                                keyboard_cancel = Keyboard(["Отмена ->"])

                                del_msg = await bot.send_message(message.from_user.id, f"Укажите название группы",
                                                                 reply_markup=keyboard_cancel.create_keyboard(3))
                                list_delete_usr_set_upd.append(del_msg.message_id)

                                await state.update_data(user_settings_status_group=1)
                                await QuestionParams.user_settings_update.set()

                            match state_data["user_settings_status_group"]:

                                case 1:
                                    if len(answer) > 9:
                                        except__ = 1
                                        raise ValueError

                                    for i in params_user["user_group"]['dict_1'].items():

                                        if i[0] == answer:
                                            except__ = 2
                                            raise ValueError

                                        if answer.lower() == "default" or answer.lower() == "all":
                                            except__ = 4
                                            raise ValueError
                                    else:
                                        key_set = Keyboard(buttons_settings_menu)
                                        msg = handlers_dict['user_settings_update_accept_g']

                                        del_msg = await bot.send_message(message.from_user.id,
                                                                         f"{msg} {answer}",
                                                                         reply_markup=key_set.create_keyboard(4))
                                        list_delete_usr_set_upd.append(del_msg.message_id)

                                        params_user["user_group"]['dict_1'][f"{answer}"] = "❌"
                                        params_user["user_group"]['dict_2'][f"{answer}"] = "❌"

                                        await state.update_data(user_settings_status_group=0)

                        elif state_data["user_settings_button_update"] == "Изменить группу ->" or \
                                state_data["user_settings_button_update"] == "Удалить группу ->":

                            if state_data["user_settings_status_group"] == 1 or \
                                    state_data["user_settings_status_group"] == 2:
                                pass

                            else:
                                keyboard_cancel = Keyboard(["Отмена ->"])
                                del_msg = ""

                                if state_data["user_settings_button_update"] == "Изменить группу ->":
                                    del_msg = await bot.send_message(message.from_user.id,
                                                                     f"Укажите название группы которую хотите изменить",
                                                                     reply_markup=keyboard_cancel.create_keyboard(3))

                                elif state_data["user_settings_button_update"] == "Удалить группу ->":
                                    del_msg = await bot.send_message(message.from_user.id,
                                                                     f"Укажите название группы которую хотите удалить",
                                                                     reply_markup=keyboard_cancel.create_keyboard(3))

                                list_delete_usr_set_upd.append(del_msg.message_id)

                                await state.update_data(user_settings_status_group=1)
                                await QuestionParams.user_settings_update.set()

                            match state_data["user_settings_status_group"]:

                                case 1:
                                    if len(answer) > 9:
                                        except__ = 1
                                        raise ValueError
                                    cont_ = 0

                                    for i in params_user["user_group"]['dict_1'].items():
                                        if i[0] == answer:
                                            cont_ = 1

                                        if answer.lower() == "default" or answer.lower() == "all":
                                            except__ = 4
                                            raise ValueError

                                    if cont_ == 0:
                                        except__ = 3
                                        raise ValueError

                                    if cont_ == 1:
                                        del_msg = ""

                                        if state_data["user_settings_button_update"] == "Изменить группу ->":
                                            del_msg = await bot.send_message(message.from_user.id,
                                                                             f"Укажите новое название группы")

                                            await state.update_data(name_del_group=answer)
                                            await state.update_data(user_settings_status_group=2)

                                        elif state_data["user_settings_button_update"] == "Удалить группу ->":

                                            key_set = Keyboard(buttons_settings_menu)

                                            del_msg = await bot.send_message(message.from_user.id,
                                                                             f"Настройки сохранены. "
                                                                             f"Группа : {answer} удалена.\n"
                                                                             f"Все слова под этой группой перенеслись в"
                                                                             f" группу : default",
                                                                             reply_markup=key_set.create_keyboard(4))

                                            params_user["user_group"]['dict_1'].pop(answer)
                                            params_user["user_group"]['dict_2'].pop(answer)
                                            data_base.update_group_up_to_default(answer)

                                            await state.update_data(user_settings_status_group=0)

                                        list_delete_usr_set_upd.append(del_msg.message_id)

                                    await QuestionParams.user_settings_update.set()

                                case 2:

                                    keyboard_settings = Keyboard(buttons_settings_menu)
                                    del_msg = ""

                                    if state_data["user_settings_button_update"] == "Изменить группу ->":
                                        del_msg = await bot.send_message(message.from_user.id,
                                                                         f"Настройки сохранены. "
                                                                         f"Название группы изменено на : "
                                                                         f"{answer}",
                                                                         reply_markup=keyboard_settings.create_keyboard(
                                                                             4))

                                    elif state_data["user_settings_button_update"] == "Удалить группу ->":
                                        del_msg = await bot.send_message(message.from_user.id,
                                                                         f"Настройки сохранены. "
                                                                         f"Группа {answer} "
                                                                         f"удалена",
                                                                         reply_markup=keyboard_settings.create_keyboard(
                                                                             4))

                                    list_delete_usr_set_upd.append(del_msg.message_id)

                                    params_user["user_group"]['dict_1'].pop(state_data["name_del_group"])
                                    params_user["user_group"]['dict_2'].pop(state_data["name_del_group"])

                                    if state_data["user_settings_button_update"] == "Изменить группу ->":

                                        params_user["user_group"]['dict_1'][f"{answer}"] = "❌"
                                        params_user["user_group"]['dict_2'][f"{answer}"] = "❌"
                                        data_base.update_group_up_to_default(update_grp=answer,
                                                                             old_grp=state_data["name_del_group"])

                                    await state.update_data(user_settings_status_group=0)

                        elif state_data["user_settings_button_update"] == "Удалить группу ->":
                            pass

                        else:
                            key_set = Keyboard(buttons_settings_menu)

                            del_msg = await bot.send_message(message.from_user.id, f"Используйте только кнопки ",
                                                             reply_markup=key_set.create_keyboard(4))
                            list_delete_usr_set_upd.append(del_msg.message_id)

                except ValueError as ex:
                    except_ = 1
                    del_msg = 0

                    match except__:
                        case 0:
                            del_msg = await bot.send_message(message.from_user.id, f"Вводите числа")
                        case 1:
                            del_msg = await bot.send_message(message.from_user.id, f"Макс. длина названия 9 символов")
                        case 2:
                            del_msg = await bot.send_message(message.from_user.id, f"Такая группа уже существует")
                        case 3:
                            del_msg = await bot.send_message(message.from_user.id, f"Такой группы не существует")
                        case 4:
                            del_msg = await bot.send_message(message.from_user.id, f"Это стандартная группа, "
                                                                                   f"ее нельзя изменить или удалить")
                        case 5:
                            del_msg = await bot.send_message(message.from_user.id, f"Вводите число от 0 до 100")

                    list_delete_usr_set_upd.append(del_msg.message_id)
                    logger_(message.from_user.id, f"file: handlers/user_settings_update_4 /// {ex}")

                except ZeroDivisionError:
                    except_ = 0

                finally:

                    state_data = await state.get_data()

                    try:
                        if state_data["user_settings_status_group"] == 1 or \
                                state_data["user_settings_status_group"] == 2:
                            pass
                        else:
                            raise KeyError

                    except KeyError:
                        if except_ == 0:
                            user_settings_status = 1
                            await state.update_data(user_settings_status=0)

                data_base.update_data_(column_="params_user", data_updating=json.dumps(params_user))
                await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)

        if user_settings_status == 1:
            await QuestionParams.user_settings_update.set()

            if state_data["user_settings_update"] == "Группы ->":
                pass
            else:
                await bot.delete_message(message.chat.id, message.message_id)

            await state.update_data(list_delete_usr_set_upd=list_delete_usr_set_upd)


def register_handler_command_settings(dp: Dispatcher):
    dp.register_message_handler(user_settings, Text(equals="Настройки ->"))
    dp.register_message_handler(user_settings_update, state=QuestionParams.user_settings_update)
