from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DB import db2


def update_keyboard_secondary(button, dict_, user_id):
    """ Additional function for dynamically changing inline buttons
        Here we overwrite the second dictionary """

    data_base = db2.DB(user_id)
    status = int(data_base.status_select()[0][0])

    done = "✅"
    butt_dict_1_1 = {}

    for i in dict_.items():
        if int(i[0]) == int(button):
            match i[1][-1]:
                case " ":
                    butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
                case "✅":
                    butt_dict_1_1.update({f"{i[0]}": f"{i[1][0:-1]} "})
        else:
            butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})

    match int(button):
        case int(1):
            butt_dict_1_1.update({"2": "За все время "})
        case int(2):
            butt_dict_1_1.update({"1": "За период "})
        case int(3):
            butt_dict_1_1.update({"4": "англ --> рус "})
        case int(4):
            butt_dict_1_1.update({"3": "рус --> англ "})

    if status == 1:
        data_base.butt_dict_upd_update(butt_dict_1_1)

    elif status == 0:
        data_base.butt_dict_update(butt_dict_1_1)


def update_keyboard_main(button, user_id):
    """ Additional function for dynamically changing the inline buttons """

    data_base = db2.DB(user_id)
    status = int(data_base.status_select()[0][0])

    if status == 1:
        butt_dict = data_base.butt_dict_select()

        update_keyboard_secondary(button, butt_dict, user_id)
        data_base.status_update(0)

        return keyboard_choose(user_id)

    elif status == 0:
        butt_dict_upd = data_base.butt_dict_upd_select()

        update_keyboard_secondary(button, butt_dict_upd, user_id)
        data_base.status_update(1)

        return keyboard_choose(user_id)


def keyboard_choose(user_id):
    """ Function for dynamically changing the inline buttons in manual parameter selection mode """

    data_base = db2.DB(user_id)

    status = int(data_base.status_select()[0][0])

    param_day = data_base.select_data_(column_="param_day", where_clmn="id", where_data=1)[0][0]

    if status == 1:
        butt_dict = data_base.butt_dict_select()

        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict['1']} {param_day} дней", callback_data=f"inline_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict['2']}", callback_data=f"inline_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict['3']}", callback_data=f"inline_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict['4']}", callback_data=f"inline_4")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4)
        return inline_keyboard_choose

    elif status == 0:
        butt_dict_upd = data_base.butt_dict_upd_select()

        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict_upd['1']} {param_day} дней", callback_data=f"inline_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict_upd['2']}", callback_data=f"inline_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict_upd['3']}", callback_data=f"inline_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict_upd['4']}", callback_data=f"inline_4")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4)
        return inline_keyboard_choose


def keyboard_choose_replay(method_, user_id):
    """ Function for dynamically changing the inline buttons in manual parameter selection mode """

    data_base = db2.DB(user_id)

    status = int(data_base.status_select()[0][0])

    if status == 1:

        data = data_base.select_data_(method_=method_, pairs_all_or_one="one")

        inline_button_1 = InlineKeyboardButton(text=f"{data[0]} - {data[1]} ", callback_data=f"replay_1")
        inline_button_2 = InlineKeyboardButton(text=f"Изменить", callback_data=f"replay_2")
        inline_button_3 = InlineKeyboardButton(text=f"Удалить", callback_data=f"replay_3")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=1).add(inline_button_1)
        inline_keyboard_choose.row(inline_button_2, inline_button_3)

        data_base.status_update(0)
        data_base.update_data_(column_="temp_data", where_data=1, data_updating=f"{data[0]} - {data[1]}")

        return inline_keyboard_choose

    elif status == 0:

        data_2 = data_base.select_data_(method_=method_, pairs_all_or_one="one")

        inline_button_1 = InlineKeyboardButton(text=f"{data_2[0]} - {data_2[1]}",
                                               callback_data=f"replay_1")
        inline_button_2 = InlineKeyboardButton(text=f"Изменить", callback_data=f"replay_2")
        inline_button_3 = InlineKeyboardButton(text=f"Удалить", callback_data=f"replay_3")

        inline_keyboard_choose_2 = InlineKeyboardMarkup(row_width=1).add(inline_button_1)
        inline_keyboard_choose_2.row(inline_button_2, inline_button_3)

        data_base.status_update(1)
        data_base.update_data_(column_="temp_data", where_data=1, data_updating=f"{data_2[0]} - {data_2[1]}")

        return inline_keyboard_choose_2


def delete_accept(user_id, mode_):

    data_base = db2.DB(user_id)
    word = data_base.select_data_(column_="temp_data", where_clmn="id", where_data=1)

    match mode_:

        case "delete":
            inline_button_1 = InlineKeyboardButton(text=f"{word[0][0]}", callback_data=f"replay_1")
            inline_button_2 = InlineKeyboardButton(text=f"Да", callback_data=f"replay_4")
            inline_button_3 = InlineKeyboardButton(text=f"Нет", callback_data=f"replay_5")

            inline_keyboard_delete = InlineKeyboardMarkup(row_width=1).add(inline_button_1)
            inline_keyboard_delete.row(inline_button_2, inline_button_3)

            return inline_keyboard_delete

        case "update":
            inline_button_1 = InlineKeyboardButton(text=f"{word[0][0]}", callback_data=f"replay_1")
            inline_button_2 = InlineKeyboardButton(text=f" Изменить eng", callback_data=f"replay_6")
            inline_button_3 = InlineKeyboardButton(text=f"Изменить rus", callback_data=f"replay_7")
            inline_button_4 = InlineKeyboardButton(text=f"Отмена", callback_data=f"replay_5")

            inline_keyboard_delete = InlineKeyboardMarkup(row_width=1).add(inline_button_1)
            inline_keyboard_delete.row(inline_button_2, inline_button_3)
            inline_keyboard_delete.row(inline_button_4)

            return inline_keyboard_delete
