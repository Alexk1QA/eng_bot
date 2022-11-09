from keyboard.keyboard_bu_inline import *
from DB import db2
import sqlite3
import random


def message_(list_):
    """ Функция для формирования сообщения списка с неверными словами """

    message_out = "\n\n"
    count_word = 1

    for i in list_:
        a = f"{count_word} - {i[0][0]} / {i[0][1]}. Вы ввели - {i[1]}"
        message_out = f"{message_out + a} \n"
        count_word += 1

    return message_out


def chose_random_(user_id):
    """ Данная функция формирует список после ввода юзером настроек для вывода теста
        actual_dict_param отдает значения:
        1 - За посл неделю, 2 - За все время, 3 - рус --> англ, 4 - англ --> рус """

    actual_dict_param = []
    list_param_random = []

    for i in keyboard_choose(user_id)["inline_keyboard"]:
        for j in i:
            if j["text"][-1].startswith('✅'):
                actual_dict_param.append(j["callback_data"][-1])

    return actual_dict_param


def random_question(metod, user_id):

    period_and_EN_or_RUS = chose_random_(user_id)
    print(period_and_EN_or_RUS)

    # period_and_EN_or_RUS = [2, 3]

    if period_and_EN_or_RUS is None:
        pass
    else:

        word_rus_data_ = f"{metod}_rus"
        word_eng_data_ = f"{metod}_eng"
        date_data = f"{metod}_time_add"

        create_table = db2.DB(user_id)
        create_table.create_table()

        word_rus_data = create_table.select_data(word_rus_data_)
        word_eng_data = create_table.select_data(word_eng_data_)
        date_data = create_table.select_data(date_data)
        print(word_rus_data)

        all_list_data = []
        # list_data --> [['Яблоко', 'Apple'], ['Машина', 'Car']...]

        if int(period_and_EN_or_RUS[0]) == int(1) or int(period_and_EN_or_RUS[0]) == int(2):
            # Делаем перебор из слов за НЕДЕЛЮ

            for j in word_rus_data:
                if j[0] is None:
                    pass
                else:
                    if int(period_and_EN_or_RUS[0]) == int(1):
                        all_list_data.append([j[0], word_eng_data[word_rus_data.index(j)][0], date_data[word_rus_data.index(j)][0]])

                    elif int(period_and_EN_or_RUS[0]) == int(2):
                        all_list_data.append([j[0], word_eng_data[word_rus_data.index(j)][0]])

            if int(period_and_EN_or_RUS[0]) == int(1):
                print(all_list_data)

            elif int(period_and_EN_or_RUS[0]) == int(2):

                random_data = random.choice(all_list_data)

                return_list = [int(period_and_EN_or_RUS[1]), random_data]

                return return_list
            # return_list -->[3, [['Яблоко', 'Apple']]


# metod = "word"
# id = "476610055"
# (print(random_question(metod, id)))
