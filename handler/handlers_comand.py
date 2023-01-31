from message import message_handlers
from handler.handlers import *


async def start(message: types.Message):
    """ Start func """

    keyboard_start = Keyboard(buttons_main_menu)

    data_base = db2.DB(message.from_user.id)

    if message.text == "Главное меню":

        await bot.delete_message(message.from_user.id, message.message_id)
        await delete_message_main(message.from_user.id, [])

        del_msg_main = await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['start']}",
                                              reply_markup=keyboard_start.create_keyboard(3))
        data_base.update_data_(column_="params_user", where_data=2,
                               data_updating=json.dumps({"list_delete": [del_msg_main.message_id]}))

    else:
        await bot.send_message(message.from_user.id, f"English Bot 🇬🇧")

        del_msg_main = await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['start']}",
                                              reply_markup=keyboard_start.create_keyboard(3))
        await bot.delete_message(message.chat.id, message.message_id)

        data_base.create_table()

        try:
            await delete_message_main(message.from_user.id, [])
        except Exception as ex:
            logger_(message.from_user.id, f"file: handlers_command/start /// {ex}")

        try:
            check = int(data_base.select_data_(column_="keyboard_boot")[0][0])

            if check == 0 or check == 1:
                pass

        except Exception as ex:
            logger_(message.from_user.id, f"file: handlers_command/start /// {ex}")

            params_user = json.dumps({"param_questions": 10,
                                      "param_percent": 50,
                                      "middle_percent": [100, 1],
                                      "param_day": 7,
                                      "mode_questions": "eng",
                                      "mode_add_word": "auto",
                                      "user_group": {
                                          "status": 1,

                                          "dict_1": {
                                              "Default": "\u2705",
                                              "All": "\u274c"
                                          },
                                          "dict_2": {
                                              "Default": "\u2705",
                                              "All": "\u274c"
                                          }
                                      }
                                      })

            status_ = 1

            butt_dict = json.dumps({
                "1": "За период ",
                "2": "За все время ✅",
                "3": "англ --> рус ✅",
                "4": "рус --> англ "
            })

            butt_dict_upd = json.dumps({
                "1": "За период ",
                "2": "За все время ",
                "3": "англ --> рус ",
                "4": "рус --> англ "
            })

            data_base.insert_settings(params_user, status_, butt_dict, butt_dict_upd,
                                      json.dumps(dict(message.from_user)))

        data_base.update_data_(column_="params_user", where_data=2,
                               data_updating=json.dumps({"list_delete": [del_msg_main.message_id]}))
        data_base.update_data_(column_="params_user", where_data=3,
                               data_updating=json.dumps({"list_delete": []}))


async def info(message: types.Message):
    """ Func info"""

    await bot.delete_message(message.from_user.id, message.message_id)

    await delete_message_main(message.from_user.id, [])

    button = ["Главное меню"]
    keyboard_info = Keyboard(button)

    del_msg_main = await bot.send_message(message.from_user.id, f"{message_handlers.handlers_dict['info']}",
                                          reply_markup=keyboard_info.create_keyboard(3))

    await delete_message_main(message.from_user.id, [del_msg_main.message_id], mode="",
                              where_data_add=3)


def register_handler_commands_command(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(start, Text(equals="Главное меню"))
    dp.register_message_handler(info, commands=["info"])
