from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DB import db2
import json


def update_keyboard_secondary(button, dict_, user_id):
    """ Additional function for dynamically changing inline buttons. Here we overwrite the second dictionary

    @param button: button id on in inline keyboard for on this button
    @param dict_: old dictionary to create new dictionary with actual button
    @param user_id:  user id in telegram
    @return:
    """

    data_base = db2.DB(user_id)
    status_ = int(data_base.select_data_(column_="keyboard_boot", where_clmn="id", where_data=1)[0][0])

    done = "✅"
    butt_dict_1_1 = {}

    for i in dict_.items():

        if int(button) == 1 or int(button) == 2:
            if int(i[0]) == 1 or int(i[0]) == 2:
                match i[1][-1]:
                    case " ":
                        butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
                    case "✅":
                        butt_dict_1_1.update({f"{i[0]}": f"{i[1][0:-2]} "})
            else:
                butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})

        elif int(button) == 3 or int(button) == 4:
            if int(i[0]) == 3 or int(i[0]) == 4:
                match i[1][-1]:
                    case " ":
                        butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
                    case "✅":
                        butt_dict_1_1.update({f"{i[0]}": f"{i[1][0:-2]} "})
            else:
                butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})

    if status_ == 1:
        data_base.update_data_(
                  column_="keyboard_boot", where_clmn="id", where_data=3, data_updating=json.dumps(butt_dict_1_1))

    elif status_ == 0:
        data_base.update_data_(
                  column_="keyboard_boot", where_clmn="id", where_data=2, data_updating=json.dumps(butt_dict_1_1))


def update_keyboard_main(button, user_id):
    """ Additional function for dynamically changing the inline buttons
    @param button: button id on in inline keyboard for on this button
    @param user_id: user id in telegram
    @return: call keyboard_choose for building keyboard
    """

    data_base = db2.DB(user_id)
    status_ = int(data_base.select_data_(column_="keyboard_boot", where_clmn="id", where_data=1)[0][0])

    if status_ == 1:
        butt_dict = json.loads(data_base.select_data_(column_="keyboard_boot", where_clmn="id", where_data=2)[0][0])

        update_keyboard_secondary(button, butt_dict, user_id)
        data_base.update_data_(column_="keyboard_boot", data_updating=0)

        return keyboard_choose(user_id)

    elif status_ == 0:
        butt_dict_upd = json.loads(data_base.select_data_(column_="keyboard_boot", where_clmn="id", where_data=3)[0][0])

        update_keyboard_secondary(button, butt_dict_upd, user_id)
        data_base.update_data_(column_="keyboard_boot", data_updating=1)

        return keyboard_choose(user_id)


def keyboard_choose(user_id):
    """ Function for dynamically changing the inline buttons in manual parameter selection mode
    @param user_id: user id in telegram
    @return: object inline keyboard
    """

    data_base = db2.DB(user_id)

    status_ = int(data_base.select_data_(column_="keyboard_boot", where_clmn="id", where_data=1)[0][0])

    param_day = json.loads(data_base.select_data_(
                     column_="params_user", where_clmn="id", where_data=1)[0][0])["param_day"]

    if status_ == 1:
        butt_dict = json.loads(data_base.select_data_(column_="keyboard_boot", where_clmn="id", where_data=2)[0][0])

        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict['1']} {param_day} дней", callback_data=f"inline_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict['2']}", callback_data=f"inline_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict['3']}", callback_data=f"inline_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict['4']}", callback_data=f"inline_4")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4)
        return inline_keyboard_choose

    elif status_ == 0:
        butt_dict_upd = json.loads(data_base.select_data_(column_="keyboard_boot", where_clmn="id", where_data=3)[0][0])

        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict_upd['1']} {param_day} дней", callback_data=f"inline_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict_upd['2']}", callback_data=f"inline_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict_upd['3']}", callback_data=f"inline_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict_upd['4']}", callback_data=f"inline_4")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4)
        return inline_keyboard_choose


def keyboard_choose_replay(method_, user_id):
    """ Function for dynamically changing the inline buttons in manual parameter selection mode
    @param method_: method need from get data from DB
    @param user_id: user id in telegram
    @return: object inline keyboard
    """

    data_base = db2.DB(user_id)

    status_ = int(data_base.select_data_(column_="keyboard_boot", where_clmn="id", where_data=1)[0][0])

    if status_ == 1:
        data = data_base.select_data_(method_1=method_, pairs_all_or_one="one")

        if data is None:
            return None

        inline_button_1 = InlineKeyboardButton(text=f"{data[0]} - {data[1]} ", callback_data=f"replay_1")
        inline_button_2 = InlineKeyboardButton(text=f"Изменить", callback_data=f"replay_2")
        inline_button_3 = InlineKeyboardButton(text=f"Удалить", callback_data=f"replay_3")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=1).add(inline_button_1)
        inline_keyboard_choose.row(inline_button_2, inline_button_3)

        data_base.update_data_(column_="keyboard_boot", data_updating=0)
        data_base.update_data_(column_="temp_data", where_data=1, data_updating=f"{data[0]} - {data[1]}")

        return inline_keyboard_choose

    elif status_ == 0:
        data_2 = data_base.select_data_(method_1=method_, pairs_all_or_one="one")

        if data_2 is None:
            return None

        inline_button_1 = InlineKeyboardButton(text=f"{data_2[0]} - {data_2[1]}",
                                               callback_data=f"replay_1")
        inline_button_2 = InlineKeyboardButton(text=f"Изменить", callback_data=f"replay_2")
        inline_button_3 = InlineKeyboardButton(text=f"Удалить", callback_data=f"replay_3")

        inline_keyboard_choose_2 = InlineKeyboardMarkup(row_width=1).add(inline_button_1)
        inline_keyboard_choose_2.row(inline_button_2, inline_button_3)

        data_base.update_data_(column_="keyboard_boot", data_updating=1)
        data_base.update_data_(column_="temp_data", where_data=1, data_updating=f"{data_2[0]} - {data_2[1]}")

        return inline_keyboard_choose_2


def delete_accept(user_id, mode_):
    """
    @param user_id: user id in telegram
    @param mode_: mode with work this func
    @return: object inline keyboard
    """

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


def user_group(user_id: int, mode: str, callback_data: int = None):
    """
    @param user_id: user id in telegram
    @param mode: mode func read or write dict in params_user in DB
    @param callback_data: pass button for update
    @return: button list from inline keyboard
    """
    data_base = db2.DB(user_id)

    params_user = json.loads(data_base.select_data_(column_="params_user",
                                                    where_clmn="id", where_data=1)[0][0])
    mode_ = mode

    if mode_ == "read_only":
        return params_user

    if mode_ == "write":
        update_dict = {}

        if params_user["user_group"]['status'] == 1:
            count_button = 0

            for i in params_user['user_group']['dict_2'].items():
                count_button += 1

                for j in params_user['user_group']['dict_1']:
                    if count_button == callback_data:
                        if j[1] == "✅":
                            return None

                if count_button == callback_data:
                    update_dict.update({f"{i[0]}": f"✅"})
                else:
                    update_dict.update({f"{i[0]}": f"❌"})

            params_user['user_group']['dict_2'] = update_dict
            params_user["user_group"]['status'] = 2
            mode_ = "read"

        elif params_user["user_group"]['status'] == 2:
            count_button = 0

            for i in params_user['user_group']['dict_1'].items():
                count_button += 1

                for j in params_user['user_group']['dict_2']:
                    if count_button == callback_data:
                        if j[1] == "✅":
                            return None

                if count_button == callback_data:
                    update_dict.update({f"{i[0]}": f"✅"})
                else:
                    update_dict.update({f"{i[0]}": f"❌"})

            params_user['user_group']['dict_1'] = update_dict
            params_user["user_group"]['status'] = 1
            mode_ = "read"

    if mode_ == "read":

        inline_keyboard_user_group = InlineKeyboardMarkup(row_width=3)
        count_button = 1

        for i in params_user["user_group"][f"dict_{params_user['user_group']['status']}"].items():

            inline_button_data = InlineKeyboardButton(text=f"{i[0]} {i[1]}", callback_data=f"user_group_{count_button}")
            count_button += 1
            inline_keyboard_user_group.insert(inline_button_data)

        data_base.update_data_(column_="params_user", data_updating=json.dumps(params_user))

        return inline_keyboard_user_group
