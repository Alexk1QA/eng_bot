from aiogram.dispatcher.filters import Text
from keyboard.buttons_menu import *
from message.message_handlers import *
from aiogram import types, Dispatcher
from log.logging import logger_
from keyboard.keyboard import *
from func.func_bu import *
from bot_init import bot
from DB import db2


async def replay_questions(message: types.Message):
    """ Func replay mode """

    data_base = db2.DB(message.from_user.id)

    word_rus = len(data_base.select_data_(column_="word_rus", all_="on", start_func="on"))

    if word_rus == 100:
        del_msg_main = await bot.send_message(message.from_user.id, f"Минимальное значение слов для повторения - 10.\n"
                                                                    f"На данный момент у вас слов - {word_rus} ")
        await bot.delete_message(message.chat.id, message.message_id)

        await delete_message_main(message.from_user.id, [del_msg_main.message_id], mode="")

    else:

        await delete_message_main(message.from_user.id, [])

        await bot.delete_message(message.chat.id, message.message_id)

        keyboard_stop = Keyboard(["Закончить ->"])
        del_msg_main = await bot.send_message(message.from_user.id, f"Режим повторения",
                                              reply_markup=keyboard_stop.create_keyboard(1))

        # del_msg_2 = await bot.send_message(message.from_user.id, f"Укажите группу из которой делать выборку слов",
        #                                    reply_markup=user_group(message.from_user.id, mode="read"))
        try:
            keyboard_choose_replay_ = keyboard_choose_replay("word", message.from_user.id)
            if keyboard_choose_replay_ is None:
                raise ValueError
            del_msg = await bot.send_message(message.from_user.id, f"{handlers_dict[f'replay_word']}",
                                             reply_markup=keyboard_choose_replay_)
        except ValueError:
            del_msg = await bot.send_message(message.from_user.id, f"В данной группе нет ни одного слова")

        await delete_message_main(message.from_user.id, [del_msg_main.message_id, del_msg.message_id], mode="")

        data_base.update_data_(column_="temp_data", where_data=2, data_updating=del_msg.message_id)
        data_base.update_data_(column_="temp_data", where_data=5, data_updating=0)


async def def_finished(message: types.Message):

    await bot.delete_message(message.from_user.id, message.message_id)

    await delete_message_main(message.from_user.id, [])

    keyboard_start = Keyboard(buttons_main_menu)

    del_msg_main = await bot.send_message(message.from_user.id, f"{handlers_dict['start']}",
                                          reply_markup=keyboard_start.create_keyboard(3))

    del_msg = await bot.send_message(message.from_user.id, f"Выберите группу для работы с ней",
                                     reply_markup=user_group(message.from_user.id, mode="read"))

    await delete_message_main(message.from_user.id, [del_msg_main.message_id, del_msg.message_id])


async def delete_message_main(user_id: int, new_id_msg: list, mode: str = "del", where_data_add: int = 2,
                              del_pause_3: str = "not_pause") -> None:

    data_base = db2.DB(user_id)

    if mode == "del":
        try:
            list_delete = json.loads(data_base.select_data_(column_="params_user", where_data=2)[0][0])["list_delete"]

            if del_pause_3 == "not_pause":
                list_delete_ = json.loads(data_base.select_data_(column_="params_user",
                                                                 where_data=3)[0][0])["list_delete"]
                list_delete = list_delete + list_delete_

            await delete_message(user_id, list_delete, call_func="delete_message_main")

            data_base.update_data_(column_="params_user", where_data=2, data_updating=json.dumps({"list_delete": []}))

        except Exception as ex:
            logger_(user_id, f"file: handlers/delete_message_main /// {ex}")

    if len(new_id_msg) == 0:
        pass
    else:
        list_delete = json.loads(data_base.select_data_(column_="params_user", where_data=2)[0][0])["list_delete"]
        list_delete = list_delete + new_id_msg

        data_base.update_data_(column_="params_user", where_data=where_data_add,
                               data_updating=json.dumps({"list_delete": list_delete}))


async def delete_message(user_id: int, list_message: list, call_func: str = None, log=None) -> None:

    last_except = ""

    while True:
        if len(list_message) == 0:
            break
        else:
            try:
                del_msg = list_message.pop()
                await bot.delete_message(user_id, del_msg)

            except Exception as ex:
                last_except = ex

    if log is not None:
        logger_(user_id, f"file: handlers/delete_message/ call_func - {call_func} /// {last_except}")


def register_handler_command(dp: Dispatcher):
    dp.register_message_handler(replay_questions, Text(equals="Повторение слова ->"))
    dp.register_message_handler(def_finished, Text(equals="Закончить ->"))
