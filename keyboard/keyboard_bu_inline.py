from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DB import db2


def update_keyboard_secondary(button, dict_, user_id):
    """ Доп функция для динамического изменения инлайн кнопок
       Тут мы перезаписываем второй словарь """

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
            butt_dict_1_1.update({"1": "За посл неделю "})

        case int(3):
            butt_dict_1_1.update({"4": "англ --> рус "})

        case int(4):
            butt_dict_1_1.update({"3": "рус --> англ "})

    if status == 1:
        data_base.butt_dict_upd_update(butt_dict_1_1)

    elif status == 0:
        data_base.butt_dict_update(butt_dict_1_1)


def update_keyboard_main(button, user_id):
    """Доп функция для динамического изменения инлайн кнопок"""

    data_base = db2.DB(user_id)

    status = int(data_base.status_select()[0][0])
    print(status)

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
    """Функция для динамического изменения инлайн кнопок в ручном режиме выбора параметров"""

    data_base = db2.DB(user_id)

    status = int(data_base.status_select()[0][0])

    if status == 1:
        butt_dict = data_base.butt_dict_select()

        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict['1']}", callback_data=f"inline_button_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict['2']}", callback_data=f"inline_button_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict['3']}", callback_data=f"inline_button_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict['4']}", callback_data=f"inline_button_4")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4)
        return inline_keyboard_choose

    elif status == 0:
        butt_dict_upd = data_base.butt_dict_upd_select()

        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict_upd['1']}", callback_data=f"inline_button_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict_upd['2']}", callback_data=f"inline_button_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict_upd['3']}", callback_data=f"inline_button_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict_upd['4']}", callback_data=f"inline_button_4")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4)
        return inline_keyboard_choose
