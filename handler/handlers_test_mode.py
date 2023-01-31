from aiogram.dispatcher import FSMContext
from handler.handlers import *
from state.states import *


async def start_test(message: types.Message, state: FSMContext):
    """ Начало машины состояния """

    await delete_message_main(message.from_user.id, [])
    await bot.delete_message(message.chat.id, message.message_id)

    data_base = db2.DB(message.from_user.id)

    answer = message.text

    len_data = []
    message_print = ""

    try:
        match answer:
            case "Пройти тест: слова ->":
                len_data = len(data_base.select_data_(column_="word_rus", all_="on", start_func="on"))
                message_print = "слов"

            case "Пройти тест: фразы ->":
                len_data = len(data_base.select_data_(column_="phrase_rus", all_="on", start_func="on"))
                message_print = "фраз"
    except Exception as ex:
        logger_(message.from_user.id, f"file: handlers/start_test /// {ex}")

    if len_data == 100:

        keyboard_start = Keyboard(buttons_main_menu)
        del_msg_main = await bot.send_message(message.from_user.id,
                                              f"Минимальное значение {message_print} для начала теста - 10.\n"
                                              f"На данный момент у вас {message_print} - {len_data} ",
                                              reply_markup=keyboard_start.create_keyboard(3))

        await delete_message_main(message.from_user.id, [del_msg_main.message_id], mode="", where_data_add=3)

    else:
        param_questions = int(json.loads(data_base.select_data_(column_="params_user")[0][0])["param_questions"])
        await state.update_data(param_questions=param_questions)

        middle_percent = middle_percent_(message.from_user.id, mode="read")

        await state.update_data(param_percent=int(json.loads(data_base.select_data_(
                                column_="params_user", where_clmn="id", where_data=1)[0][0])["param_percent"]))

        len_data_2 = len(data_base.select_data_(method_1="word", word_during_period="user_period",
                                                word_during_period_len="on"))

        await state.update_data(len_data=len_data)
        await state.update_data(len_data_2=len_data_2)

        await state.update_data(count_fails=0)
        await state.update_data(count_questions=0)
        await state.update_data(status_=0)
        await state.update_data(temp_method=answer)
        await state.update_data(list_fails=[])
        await state.update_data(list_asked_data=[])

        keyboard_start_test = Keyboard(["Назад ->", "Начать ->"])

        del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict[f'start_test_word_1']}\n"
                                                               f"Количество вопросов во время теста будет: "
                                                               f"{param_questions}\n"
                                                               f"Ваш средний процент ответов: "
                                                               f"{round(middle_percent, 2)}%",
                                         reply_markup=keyboard_start_test.create_keyboard(3))

        del_msg_2 = await bot.send_message(message.from_user.id, f"Укажите группу из которой делать выборку слов",
                                           reply_markup=user_group(message.from_user.id, mode="read"))

        del_msg_3 = await bot.send_message(message.from_user.id, f"{handlers_dict[f'start_test_word_2']}",
                                           reply_markup=keyboard_choose(message.from_user.id))

        await state.update_data(list_delete=[message.message_id, del_msg.message_id, del_msg_2.message_id,
                                             del_msg_3.message_id])


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
    len_data_2 = state_data["len_data_2"]

    match answer:
        case "Назад ->":
            count_questions = param_questions

        case _:
            match status_:
                case 0:
                    pass

                case 1:
                    if answer == "Закончить ->":

                        count_questions = param_questions

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
                            del_msg_main = await bot.send_message(message.from_user.id,
                                                                  f"Тест пройден. Ваш процент ответов - 100%")
                            await delete_message_main(message.from_user.id, [del_msg_main.message_id], mode="",
                                                      where_data_add=3)

                            middle_percent_(message.from_user.id, 100, mode="write")

                        else:
                            if actual_percent > max_percent_fails:
                                list_fails = state_data["list_fails"]

                                del_msg_main = await bot.send_message(message.from_user.id,
                                                                      f"Тест НЕ пройден. Ваш процент ответов - "
                                                                      f"{str(100 - int(actual_percent))[0:5]}% "
                                                                      f"из требуемых {param_percent}%")

                                del_msg_main_2 = await bot.send_message(message.from_user.id,
                                                                        f"Слова в которых допускались ошибки: "
                                                                        f"{message_(list_fails)}")
                                await delete_message_main(message.from_user.id, [del_msg_main.message_id,
                                                                                 del_msg_main_2.message_id], mode="",
                                                          where_data_add=3)

                                middle_percent_(message.from_user.id, 100 - int(actual_percent), mode="write")

                            elif actual_percent <= max_percent_fails:
                                del_msg_main = await bot.send_message(message.from_user.id,
                                                                      f"Тест пройден. Ваш процент ответов - "
                                                                      f"{str(100 - int(actual_percent))[0:5]}% "
                                                                      f"из требуемых {param_percent}%")

                                del_msg_main_2 = await bot.send_message(message.from_user.id,
                                                                        f"Слова в которых допускались ошибки: "
                                                                        f"{message_(list_fails)}")

                                await delete_message_main(message.from_user.id, [del_msg_main.message_id,
                                                                                 del_msg_main_2.message_id], mode="",
                                                          where_data_add=3)

                                middle_percent_(message.from_user.id, 100 - int(actual_percent), mode="write")

    # Output to the main menu after the last question
    if count_questions == param_questions:

        match answer:
            case "Назад ->":

                keyboard_start = Keyboard(buttons_main_menu)

                del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                                      reply_markup=keyboard_start.create_keyboard(3))

                await delete_message_main(message.from_user.id, [del_msg_main.message_id])

                finally_state_data = await state.get_data()

                await delete_message(message.chat.id, finally_state_data["list_delete"],
                                     call_func="question_test_1")

                await state.finish()

            case _:

                keyboard_start = Keyboard(buttons_main_menu)

                del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                                      reply_markup=keyboard_start.create_keyboard(3))

                await delete_message_main(message.from_user.id, [del_msg_main.message_id], del_pause_3="pause")

                finally_state_data = await state.get_data()

                if finally_state_data != 0:
                    await delete_message(message.chat.id, finally_state_data["list_delete"],
                                         call_func="question_test_2")
                else:
                    pass

                await state.finish()

    else:
        list_delete = state_data["list_delete"]
        keyboard_stop = Keyboard(["Закончить ->"])

        match temp_method:
            case "Пройти тест: слова ->":

                data_ = check_word_phrase_replay("word", message.from_user.id, list_asked_data, len_data, len_data_2)

                if data_ is None:
                    pass
                else:
                    list_asked_data.append(data_[1][0])
                    await state.update_data(list_asked_data=list_asked_data)

                match data_:
                    case None:
                        del_msg = await bot.send_message(message.from_user.id, f"За указанный период нет добавленных "
                                                                               f"слов")
                        list_delete.append(del_msg.message_id)

                    case _:
                        match data_[0]:
                            case int(3):
                                # "3": "rus --> eng "
                                del_msg = await bot.send_message(message.from_user.id,
                                                                 f"Как переводится слово {data_[1][0]}",
                                                                 reply_markup=keyboard_stop.create_keyboard(1))
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
                                                                 reply_markup=keyboard_stop.create_keyboard(1))
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

                data_ = check_word_phrase_replay("phrase", message.from_user.id, list_asked_data, len_data, len_data_2)

                if data_ is None:
                    pass
                else:
                    list_asked_data.append(data_[1][0])
                    await state.update_data(list_asked_data=list_asked_data)

                match data_:
                    case None:
                        del_msg = await bot.send_message(message.from_user.id, f"Укажите период и режим работы теста ")
                        list_delete.append(del_msg.message_id)

                    case _:
                        match data_[0]:
                            case int(3):
                                # "3": "rus --> eng "
                                del_msg = await bot.send_message(message.from_user.id,
                                                                 f"Как переводится фраза {data_[1][0]}",
                                                                 reply_markup=keyboard_stop.create_keyboard(1))
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
                                                                 reply_markup=keyboard_stop.create_keyboard(1))
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


def register_handler_command_test_mode(dp: Dispatcher):

    dp.register_message_handler(start_test, Text(equals="Пройти тест: слова ->"))
    dp.register_message_handler(start_test, Text(equals="Пройти тест: фразы ->"))

    dp.register_message_handler(question_test, Text(equals="Начать ->"))
    dp.register_message_handler(question_test, Text(equals="Назад ->"))

    dp.register_message_handler(question_test, state=QuestionParams.question_test)
