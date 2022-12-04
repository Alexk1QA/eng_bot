from handler.handlers import delete_message
from aiogram.dispatcher import FSMContext
from keyboard.keyboard_bu_inline import *
from aiogram.types import CallbackQuery
from message.message_handlers import *
from aiogram import types, Dispatcher
from state.states import *
from bot_init import bot


async def manual(call: CallbackQuery):
    # Change keyboard for test mode

    numb_button = call.data[-1]

    await call.message.edit_reply_markup(update_keyboard_main(numb_button, call.message.chat.id))

    await bot.answer_callback_query(call.id, text='✅')


async def replay_questions(call: CallbackQuery, state: FSMContext):
    # Change word for replay mode

    numb_button = int(call.data[-1])

    data_base = db2.DB(call.message.chat.id)
    len_items_in_DB = len(data_base.select_data_(column_="word_eng", all_="on"))

    match numb_button:

        case 1:
            # Button Change pair words (end-rus)

            if len_items_in_DB == 0:
                await bot.answer_callback_query(call.id, text=f"Вы удалили все слова")

            else:
                await bot.answer_callback_query(call.id, text='✅')
                await call.message.edit_reply_markup(keyboard_choose_replay("word", call.message.chat.id))

        case 2:
            # Button Update words user
            await call.message.edit_reply_markup(delete_accept(call.message.chat.id, "update"))

        case 3:
            # Button delete
            await call.message.edit_reply_markup(delete_accept(call.message.chat.id, "delete"))

        case 4:
            # Button Yes from delete word
            if len_items_in_DB == 0:
                await bot.answer_callback_query(call.id, text=f"Вы удалили все слова")

            else:
                if len_items_in_DB == 0:
                    await bot.answer_callback_query(call.id, text=f"Вы удалили все слова")

                else:
                    word = data_base.select_data_(column_="temp_data", where_clmn="id", where_data=1)
                    await bot.answer_callback_query(call.id, text=f"Слово: {word[0][0]} удалено")

                    data_base.delete_data(word[0][0].split(" ")[0])

                    len_items_in_DB = len(data_base.select_data_(column_="word_eng", all_="on"))

                    if len_items_in_DB == 0:
                        await bot.answer_callback_query(call.id, text=f"Вы удалили все слова")
                        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

                    else:
                        await call.message.edit_reply_markup(keyboard_choose_replay("word", call.message.chat.id))

        case 5:
            # Button No from delete word

            if len_items_in_DB == 0:
                await bot.answer_callback_query(call.id, text=f"Вы удалили все слова")

            else:
                await call.message.edit_reply_markup(keyboard_choose_replay("word", call.message.chat.id))

        case 6:
            # Button Yes Update word from user eng

            del_msg = await bot.send_message(call.from_user.id, f"Введи правильный перевод", )
            await state.update_data(del_msg=del_msg.message_id)
            await state.update_data(method="eng")
            await QuestionParams.update_word.set()

        case 7:
            # Button Yes Update word from user rus

            del_msg = await bot.send_message(call.from_user.id, f"Введи правильный перевод", )
            await state.update_data(del_msg=del_msg.message_id)
            await state.update_data(method="rus")
            await QuestionParams.update_word.set()


async def update_word(message: types.Message, state: FSMContext):
    answer = message.text

    state_data = await state.get_data()
    del_msg = state_data["del_msg"]
    method_ = state_data["method"]

    data_base = db2.DB(message.chat.id)

    word = data_base.select_data_(column_="temp_data", where_clmn="id", where_data=1)

    match method_:

        case "eng":
            word = word[0][0].split(" ")[0]

        case "rus":
            word = word[0][0].split(" ")[-1]

    # data_base.update_data_for_user(word, answer, method_)
    data_base.update_data_(method_=method_, where_data=word, data_updating=answer)

    await delete_message(
        message.chat.id, [message.message_id, state_data["del_msg"],
                          data_base.select_data_(column_='temp_data', where_clmn="id", where_data=2)[0][0]])

    del_msg = await bot.send_message(message.from_user.id,
                                     f"update_word {handlers_dict[f'replay_word']}",
                                     reply_markup=keyboard_choose_replay("word", message.chat.id))

    if int(data_base.select_data_(column_="temp_data", where_clmn="id", where_data=5)[0][0]) == 0:

        data_base.update_data_(column_="temp_data", where_data=3, data_updating=del_msg.message_id)
        data_base.update_data_(column_="temp_data", where_data=5, data_updating=1)

        await delete_message(message.from_user.id, [data_base.select_data_(column_='temp_data', where_clmn="id", where_data=4)[0][0]])

    else:
        data_base.update_data_(column_="temp_data", where_data=4, data_updating=del_msg.message_id)
        data_base.update_data_(column_="temp_data", where_data=5, data_updating=0)

        await delete_message(message.from_user.id, [data_base.select_data_(column_='temp_data', where_clmn="id", where_data=3)[0][0]])

    await state.finish()


def register_handler_command_bu_inline(dp: Dispatcher):
    dp.register_callback_query_handler(manual, lambda c: c.data.startswith('inline'))
    dp.register_callback_query_handler(replay_questions, lambda c: c.data.startswith('replay'))
    dp.register_message_handler(update_word, state=QuestionParams.update_word)
