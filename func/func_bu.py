from keyboard.keyboard_bu_inline import *
from datetime import datetime, timedelta
import datetime as dt
from DB import db2
import random


def message_(list_):
    """ Функция для формирования сообщения списка с неверными словами """

    message_out = "\n\n"
    count_word = 1

    for i in list_:
        a = f"{count_word} - {i[0][0]} / {i[0][1]}. Вы ввели - «{i[1]}»"
        message_out = f"{message_out + a} \n"
        count_word += 1

    return message_out


def chose_random_(user_id):
    """ Данная функция формирует список после ввода юзером настроек для вывода теста
        actual_dict_param отдает значения:
        1 - За посл неделю, 2 - За все время, 3 - рус --> англ, 4 - англ --> рус """

    actual_dict_param = []

    for i in keyboard_choose(user_id)["inline_keyboard"]:
        for j in i:
            if j["text"][-1].startswith('✅') or j["text"][-8].startswith('✅'):
                actual_dict_param.append(j["callback_data"][-1])

    return actual_dict_param


def random_question(method_, user_id, mode_func):

    period_and_EN_or_RUS = chose_random_(user_id)
    # example period_and_EN_or_RUS --> [2, 3]

    if period_and_EN_or_RUS is None:
        pass

    else:
        word_rus_data_ = f"{method_}_rus"
        word_eng_data_ = f"{method_}_eng"
        date_data = f"{method_}_time_add"

        data_base = db2.DB(user_id)
        data_base.create_table()

        word_rus_data = data_base.select_data(word_rus_data_)
        word_eng_data = data_base.select_data(word_eng_data_)
        date_data = data_base.select_data(date_data)

        all_list_data = []

        if mode_func == 1:
            period_and_EN_or_RUS = [2, 2]

        if int(period_and_EN_or_RUS[0]) == int(1) or int(period_and_EN_or_RUS[0]) == int(2):
            # Делаем перебор из слов за НЕДЕЛЮ

            for j in word_rus_data:
                if j[0] is None:
                    pass
                else:
                    if int(period_and_EN_or_RUS[0]) == int(1):
                        all_list_data.append([j[0], word_eng_data[word_rus_data.index(j)][0],
                                              date_data[word_rus_data.index(j)][0]])
            # example [['Яблоко', 'Apple', 'Wed Nov  9 19:56:04 2022'], ['www', 'www', 'Wed Nov  9 19:56:32 2022']...]

                    elif int(period_and_EN_or_RUS[0]) == int(2):
                        all_list_data.append([j[0], word_eng_data[word_rus_data.index(j)][0]])
                        # example [['Яблоко', 'Apple'], ['Машина', 'Car']...]
            if mode_func == 1:
                # with open(f'/Users/macbook/Desktop/english_bot/temporary/words_id_{user_id}.txt', 'w') as file:
                with open(f'/home/ubuntu/eng_bot/temporary/words_id_{user_id}.txt', 'w') as file:
                    file.writelines(f'{row[1]} - {row[0]}\n' for row in all_list_data)

                return file

            else:
                if int(period_and_EN_or_RUS[0]) == int(1):

                    param_day = "param_day"
                    param_date = data_base.select_data(param_day)[0][0]

                    mod_date = datetime.now() + timedelta(days=-param_date)
                    data = str(mod_date.date())
                    range_date_str = data[8:10] + data[4:8] + data[0:4]

                    list_range = []

                    for i in all_list_data:
                        items_in_list = i[2][0:6] + "20" + i[2][6:8]

                        range_date_str_ = dt.datetime.strptime(range_date_str, '%d-%m-%Y')
                        items_in_list_ = dt.datetime.strptime(items_in_list, '%d-%m-%Y')

                        if range_date_str_ <= items_in_list_:
                            list_range.append([i[0], i[1]])

                    random_data = random.choice(list_range)

                    return_list = [int(period_and_EN_or_RUS[1]), random_data]

                    return return_list
                    # return_list -->[3, [['Яблоко', 'Apple']]

                elif int(period_and_EN_or_RUS[0]) == int(2):

                    random_data = random.choice(all_list_data)

                    return_list = [int(period_and_EN_or_RUS[1]), random_data]

                    return return_list
                    # return_list -->[3, [['Яблоко', 'Apple']]
