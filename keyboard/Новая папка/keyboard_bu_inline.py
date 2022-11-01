from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

global butt_dict_1

button_test_1 = KeyboardButton("Test")
keyboard_Test_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_test_1)


button_Choose_Continue = KeyboardButton("Продолжить")
keyboard_Choose_Continue = ReplyKeyboardMarkup(resize_keyboard=True).add(button_Choose_Continue)

status = 1
butt_dict = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "0": "0"
}

butt_dict_upd = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "0": "0"
}


def update_keyboard_secondary(button, dict_):
    """Доп функция для динамического изменения инлайн кнопок
       Тут мы перезаписываем второй словарь и делаем проверку на кнопки 2, 3, 4, 5,
       что они отмечены в правильном порядке
    """

    global butt_dict_upd, status, butt_dict


    done = "✅"
    butt_dict_1_1 = {}

    for i in dict_:
        if int(i) == int(button):
            if len(dict_[i]) == 1:
                butt_dict_1_1.update({f"{i}": f"{i} {done}"})
            elif len(dict_[i]) > 1:
                butt_dict_1_1.update({f"{i}": f"{i}"})
        else:
            butt_dict_1_1.update({f"{i}": f"{dict_[i]}"})

    if int(button) == 3 or int(button) == 5:
        if len(butt_dict[f"{button}"]) == 1:
            if len(butt_dict[f"{int(button) - 1}"]) == 1:
                butt_dict_1_1.update({f"{int(button) - 1}": f"{int(button) - 1} {done}"})

        if len(butt_dict_upd[f"{button}"]) == 1:
            if len(butt_dict_upd[f"{int(button) - 1}"]) == 1:
                butt_dict_1_1.update({f"{int(button) - 1}": f"{int(button) - 1} {done}"})

    elif int(button) == 2 or int(button) == 4:
        if len(butt_dict[f"{button}"]) > 1:
            if len(butt_dict[f"{int(button) + 1}"]) > 1:
                butt_dict_1_1.update({f"{int(button) + 1}": f"{int(button) + 1}"})

        if len(butt_dict_upd[f"{button}"]) > 1:
            if len(butt_dict_upd[f"{int(button) + 1}"]) > 1:
                butt_dict_1_1.update({f"{int(button) + 1}": f"{int(button) + 1}"})

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
        inline_button_5 = InlineKeyboardButton(text=f"{butt_dict['5']}", callback_data=f"inline_button_5")
        inline_button_6 = InlineKeyboardButton(text=f"{butt_dict['6']}", callback_data=f"inline_button_6")
        inline_button_7 = InlineKeyboardButton(text=f"{butt_dict['7']}", callback_data=f"inline_button_7")
        inline_button_8 = InlineKeyboardButton(text=f"{butt_dict['8']}", callback_data=f"inline_button_8")
        inline_button_9 = InlineKeyboardButton(text=f"{butt_dict['9']}", callback_data=f"inline_button_9")
        inline_button_0 = InlineKeyboardButton(text=f"1{butt_dict['0']}", callback_data=f"inline_button_0")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=3).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4,
                                                                       inline_button_5, inline_button_6,
                                                                       inline_button_7, inline_button_8,
                                                                       inline_button_9, inline_button_0)
    elif status == 0:
        inline_button_1 = InlineKeyboardButton(text=f"{butt_dict_upd['1']}", callback_data=f"inline_button_1")
        inline_button_2 = InlineKeyboardButton(text=f"{butt_dict_upd['2']}", callback_data=f"inline_button_2")
        inline_button_3 = InlineKeyboardButton(text=f"{butt_dict_upd['3']}", callback_data=f"inline_button_3")
        inline_button_4 = InlineKeyboardButton(text=f"{butt_dict_upd['4']}", callback_data=f"inline_button_4")
        inline_button_5 = InlineKeyboardButton(text=f"{butt_dict_upd['5']}", callback_data=f"inline_button_5")
        inline_button_6 = InlineKeyboardButton(text=f"{butt_dict_upd['6']}", callback_data=f"inline_button_6")
        inline_button_7 = InlineKeyboardButton(text=f"{butt_dict_upd['7']}", callback_data=f"inline_button_7")
        inline_button_8 = InlineKeyboardButton(text=f"{butt_dict_upd['8']}", callback_data=f"inline_button_8")
        inline_button_9 = InlineKeyboardButton(text=f"{butt_dict_upd['9']}", callback_data=f"inline_button_9")
        inline_button_0 = InlineKeyboardButton(text=f"1{butt_dict_upd['0']}", callback_data=f"inline_button_0")

        inline_keyboard_choose = InlineKeyboardMarkup(row_width=3).add(inline_button_1, inline_button_2,
                                                                       inline_button_3, inline_button_4,
                                                                       inline_button_5, inline_button_6,
                                                                       inline_button_7, inline_button_8,
                                                                       inline_button_9, inline_button_0)
    return inline_keyboard_choose












