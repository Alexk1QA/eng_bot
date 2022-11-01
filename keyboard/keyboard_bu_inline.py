from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


button_test_1 = KeyboardButton("Test")
keyboard_Test_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_test_1)


button_Choose_Continue = KeyboardButton("Продолжить")
keyboard_Choose_Continue = ReplyKeyboardMarkup(resize_keyboard=True).add(button_Choose_Continue)

status = 1
butt_dict = {
        "1": "За посл неделю ",
        "2": "За все время ",
        "3": "рус --> англ ",
        "4": "англ --> рус "
}

butt_dict_upd = {
         "1": "За посл неделю ",
         "2": "За все время ",
         "3": "рус --> англ ",
         "4": "англ --> рус "
}


def update_keyboard_secondary(button, dict_):
    """ Доп функция для динамического изменения инлайн кнопок
       Тут мы перезаписываем второй словарь """

    global butt_dict_upd, status, butt_dict

    done = "✅"
    butt_dict_1_1 = {}

    for i in dict_.items():
        # match int(i[0]):
        if int(i[0]) == int(button):
            # case int(buttton):
            match i[1][-1]:
                case " ":
                        butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
                case "✅":
                        butt_dict_1_1.update({f"{i[0]}": f"{i[1][0:-1]} "})
        else:
            butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})

    match int(button):

        case int(1):
            butt_dict_1_1.update({"2": "За посл неделю "})

        case int(2):
            butt_dict_1_1.update({"1": "За все время "})

        case int(3):
            butt_dict_1_1.update({"4": "англ --> рус "})

        case int(4):
            butt_dict_1_1.update({"3": "рус --> англ "})

    if status == 1:
        butt_dict_upd = butt_dict_1_1
        return butt_dict_upd
    elif status == 0:
        butt_dict = butt_dict_1_1
        return butt_dict


def update_keyboard_main(button):
    """Доп функция для динамического изменения инлайн кнопок"""

    global status

    if status == 1:
        actual_dict = update_keyboard_secondary(button, butt_dict)
        status = 0
        return actual_dict
    elif status == 0:
        actual_dict = update_keyboard_secondary(button, butt_dict_upd)
        status = 1
        return actual_dict


def keyboard_choose():
    """Функция для динамического изменения инлайн кнопок в ручном режиме выбора параметров"""
    global inline_keyboard_choose, status

    if status == 1:
        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict['1']}", callback_data=f"inline_button_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict['2']}", callback_data=f"inline_button_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict['3']}", callback_data=f"inline_button_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict['4']}", callback_data=f"inline_button_4")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4)
    elif status == 0:
        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict_upd['1']}", callback_data=f"inline_button_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict_upd['2']}", callback_data=f"inline_button_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict_upd['3']}", callback_data=f"inline_button_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict_upd['4']}", callback_data=f"inline_button_4")


        inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4)
    return inline_keyboard_choose












