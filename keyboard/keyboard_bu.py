from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from message.message_handlers import *
import random

global car

button_test = KeyboardButton("Тестовая кнопка")
keyboard_Test = ReplyKeyboardMarkup(resize_keyboard=True).add(button_test)

button_Main_Menu = KeyboardButton("Главное меню ")
button_Back_in_Machine = KeyboardButton("Назад")

button_continiue = KeyboardButton("Выполнить запрос")
keyboard_continiue = ReplyKeyboardMarkup(resize_keyboard=True).add(button_continiue)


def keyboard_start_bu():
    """Клавиатуры выбора параметров"""

    button_4_Param = KeyboardButton("4")
    button_7_Param = KeyboardButton("7")
    button_10_Param = KeyboardButton("10")
    button_Chose_Param = KeyboardButton("Ввести параметры вручную")

    keyboard_start_bu_ = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(button_4_Param, button_7_Param,
                                                                                    button_10_Param)
    keyboard_start_bu_.row(button_Chose_Param)
    keyboard_start_bu_.row(button_Main_Menu)

    return keyboard_start_bu_


def keyboard_Accept_Param():
    """Клавиатура подтверждения ручного вода"""

    button_Accept_Param = KeyboardButton("Продолжить ->")

    keyboard_Accept_Param_ = ReplyKeyboardMarkup(resize_keyboard=True).add(button_Accept_Param)

    keyboard_Accept_Param_.row(button_Back_in_Machine)
    keyboard_Accept_Param_.row(button_Main_Menu)

    return keyboard_Accept_Param_


def keyboard_region():
    """Клавиатура выбора региона """

    dict_region_out = {}
    random_list = []

    name_button = test_region()[1]

    for i in name_button:
        if i == f"{handlers_bu_dict['region_top'][0]}" or \
                i == f"{handlers_bu_dict['region_top'][1]}" or i == f"{handlers_bu_dict['region_top'][2]}":
            pass
        else:
            dict_region_out.update({f"{i}": f"{name_button[i]}"})

    for i in range(1, 200):
        items = random.choice(list(dict_region_out))
        if len(random_list) < 6:
            if items not in random_list:
                random_list.append(items)

    button_region_1 = KeyboardButton(f"{handlers_bu_dict['region_top'][0]}")
    button_region_2 = KeyboardButton(f"{handlers_bu_dict['region_top'][1]}")
    button_region_3 = KeyboardButton(f"{handlers_bu_dict['region_top'][2]}")
    button_region_4 = KeyboardButton(f"{random_list[0]}")
    button_region_5 = KeyboardButton(f"{random_list[1]}")
    button_region_6 = KeyboardButton(f"{random_list[2]}")
    button_region_7 = KeyboardButton(f"{random_list[3]}")
    button_region_8 = KeyboardButton(f"{random_list[4]}")
    button_region_9 = KeyboardButton(f"{random_list[5]}")

    keyboard_region_ = ReplyKeyboardMarkup(resize_keyboard=True).add(button_region_1, button_region_2, button_region_3,
                                                                     button_region_4, button_region_5, button_region_6,
                                                                     button_region_7, button_region_8, button_region_9)

    keyboard_region_.row(button_Main_Menu)

    return keyboard_region_


def keyboard_category():
    """ Клавиатура выбора типа транспорта """
    dict_category_all = test_category()[1]

    keyboard_category_ = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add()
    count = 0
    for items in dict_category_all:
        if count > 8:
            pass
        else:
            dict_category_all[f'{items}'] = KeyboardButton(f"{items}")
            keyboard_category_.insert(dict_category_all[f'{items}'])
            count += 1

    keyboard_category_.row(button_Main_Menu)

    return keyboard_category_


def keyboard_body(category):
    """ Клавиатура выбора типа кузова транспорта """

    dict_body_all = test_body(category)[1]

    if category == "Автобусы" or category == "Автодома" or category == "Воздушный транспорт":

        dict_body_all = test_body(category)[1]

        keyboard_body_ = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add()
        count = 0
        for items in dict_body_all:
            if count > 8:
                pass
            else:
                dict_body_all[f'{items}'] = KeyboardButton(f"{items}")
                keyboard_body_.insert(dict_body_all[f'{items}'])
                count += 1

        keyboard_body_.row(button_Main_Menu)

        return keyboard_body_

    else:
        name_button = del_param_body(category, dict_body_all)
        print(name_button)

        button_body_1 = KeyboardButton(f"{handlers_bu_dict[f'top_body_{category}'][0]}")
        button_body_2 = KeyboardButton(f"{handlers_bu_dict[f'top_body_{category}'][1]}")
        button_body_3 = KeyboardButton(f"{handlers_bu_dict[f'top_body_{category}'][2]}")
        button_body_4 = KeyboardButton(f"{name_button[0]}")
        button_body_5 = KeyboardButton(f"{name_button[1]}")
        button_body_6 = KeyboardButton(f"{name_button[2]}")
        button_body_7 = KeyboardButton(f"{name_button[3]}")
        button_body_8 = KeyboardButton(f"{name_button[4]}")
        button_body_9 = KeyboardButton(f"{name_button[5]}")

        keyboard_body_ = ReplyKeyboardMarkup(resize_keyboard=True).add(button_body_1, button_body_2, button_body_3,
                                                                       button_body_4, button_body_5, button_body_6,
                                                                       button_body_7, button_body_8, button_body_9)

        keyboard_body_.row(button_Main_Menu)

        return keyboard_body_


def del_param_body(category, dict_body_in):
    """ Доп функция клавиатуры body"""
    dict_body_out = {}
    random_list = []

    dict_category = {
        "Легковые": "1",
        "Мото": "2",
        "Водный транспорт": "3",
        "Спецтехника": "4",
        "Прицепы": "5",
        "Грузовики": "6",
        "Сельхозтехника": "10"
    }

    if dict_category.get(category):
        for i in dict_body_in:
            if i == f"{handlers_bu_dict[f'top_body_{category}'][0]}" or \
                    i == f"{handlers_bu_dict[f'top_body_{category}'][1]}" or \
                    i == f"{handlers_bu_dict[f'top_body_{category}'][2]}":
                pass
            else:
                dict_body_out.update({f"{i}": f"{dict_body_in[i]}"})

        for i in range(1, 200):
            items = random.choice(list(dict_body_out))
            if len(random_list) < 6:
                if items not in random_list:
                    random_list.append(items)

        return random_list


def keyboard_marka(category):
    """Клавиатура выбора марок """

    dict_marka_all = test_marka(category)[1]

    name_button = del_param_marka(category, dict_marka_all)
    print(name_button)

    button_marka_1 = KeyboardButton(f"{handlers_bu_dict[f'top_marka_{category}'][0]}")
    button_marka_2 = KeyboardButton(f"{handlers_bu_dict[f'top_marka_{category}'][1]}")
    button_marka_3 = KeyboardButton(f"{handlers_bu_dict[f'top_marka_{category}'][2]}")
    button_marka_4 = KeyboardButton(f"{name_button[0]}")
    button_marka_5 = KeyboardButton(f"{name_button[1]}")
    button_marka_6 = KeyboardButton(f"{name_button[2]}")
    button_marka_7 = KeyboardButton(f"{name_button[3]}")
    button_marka_8 = KeyboardButton(f"{name_button[4]}")
    button_marka_9 = KeyboardButton(f"{name_button[5]}")

    keyboard_marka_ = ReplyKeyboardMarkup(resize_keyboard=True).add(button_marka_1, button_marka_2, button_marka_3,
                                                                    button_marka_4, button_marka_5, button_marka_6,
                                                                    button_marka_7, button_marka_8, button_marka_9)

    keyboard_marka_.row(button_Main_Menu)

    return keyboard_marka_


def del_param_marka(category, dict_body_in):
    """ Доп функция клавиатуры marka"""
    dict_body_out = {}
    random_list = []

    dict_category = {
        "Легковые": "1",
        "Мото": "2",
        "Водный транспорт": "3",
        "Спецтехника": "4",
        "Прицепы": "5",
        "Грузовики": "6",
        "Автобусы": "7",
        "Автодома": "8",
        "Воздушный транспорт": "9",
        "Сельхозтехника": "10"
    }

    if dict_category.get(category):
        for i in dict_body_in:
            if i == f"{handlers_bu_dict[f'top_marka_{category}'][0]}" or \
                    i == f"{handlers_bu_dict[f'top_marka_{category}'][1]}" or \
                    i == f"{handlers_bu_dict[f'top_marka_{category}'][2]}":
                pass
            else:
                dict_body_out.update({f"{i}": f"{dict_body_in[i]}"})

        for i in range(1, 200):
            items = random.choice(list(dict_body_out))
            if len(random_list) < 6:
                if items not in random_list:
                    random_list.append(items)

        return random_list


def keyboard_model(category, marka):
    """ Клавиатура Выбора моделей  """

    random_button = []

    dict_model_all = test_model(category, marka)[1]

    if len(dict_model_all) < 8:

        dict_body_all = test_model(category, marka)[1]

        keyboard_model_ = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add()
        count = 0
        for items in dict_body_all:
            if count > 8:
                pass
            else:
                dict_body_all[f'{items}'] = KeyboardButton(f"{items}")
                keyboard_model_.insert(dict_body_all[f'{items}'])
                count += 1

        keyboard_model_.row(button_Main_Menu)

        return keyboard_model_

    else:
        for i in range(1, 200):
            items = random.choice(list(dict_model_all))
            if len(random_button) < 9:
                if items not in random_button:
                    random_button.append(items)

        button_model_1 = KeyboardButton(f"{random_button[0]}")
        button_model_2 = KeyboardButton(f"{random_button[1]}")
        button_model_3 = KeyboardButton(f"{random_button[2]}")
        button_model_4 = KeyboardButton(f"{random_button[3]}")
        button_model_5 = KeyboardButton(f"{random_button[4]}")
        button_model_6 = KeyboardButton(f"{random_button[5]}")
        button_model_7 = KeyboardButton(f"{random_button[6]}")
        button_model_8 = KeyboardButton(f"{random_button[7]}")
        button_model_9 = KeyboardButton(f"{random_button[8]}")

        keyboard_model_ = ReplyKeyboardMarkup(resize_keyboard=True).add(button_model_1, button_model_2, button_model_3,
                                                                        button_model_4, button_model_5, button_model_6,
                                                                        button_model_7, button_model_8, button_model_9)

        keyboard_model_.row(button_Main_Menu)

        return keyboard_model_


def keyboard_year_price():
    """ Клавиатуры машины состояния года и цены """

    button_from_year = KeyboardButton("Главное меню")
    keyboard_year_price_ = ReplyKeyboardMarkup(resize_keyboard=True).add(button_from_year)

    return keyboard_year_price_


def keyboard_fuel():
    """ Клавиатура типа топлива """

    dict_fuel_all = test_fuel()[1]

    keyboard_fuel_ = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add()
    count = 0
    for items in dict_fuel_all:
        if count > 8:
            pass
        else:
            dict_fuel_all[f'{items}'] = KeyboardButton(f"{items}")
            keyboard_fuel_.insert(dict_fuel_all[f'{items}'])
            count += 1

    keyboard_fuel_.row(button_Main_Menu)

    return keyboard_fuel_


def keyboard_kpp():
    """ Клавиатура выбора коробки передач """

    dict_body_all = test_kpp()[1]

    keyboard_kpp_ = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add()
    count = 0
    for items in dict_body_all:
        if count > 8:
            pass
        else:
            dict_body_all[f'{items}'] = KeyboardButton(f"{items}")
            keyboard_kpp_.insert(dict_body_all[f'{items}'])
            count += 1

    keyboard_kpp_.row(button_Main_Menu)

    return keyboard_kpp_


def keyboard_volume(category):
    """ Клавиатура обьема двигателя """

    keyboard_kpp_ = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add()
    count = 0
    for items in handlers_bu_dict[f'button_volume_{category}']:
        if count > 8:
            pass
        else:
            keyboard_kpp_.insert(items)
            count += 1

    keyboard_kpp_.row(button_Main_Menu)

    return keyboard_kpp_

