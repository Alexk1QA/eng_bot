from keyboard.keyboard_bu_inline import *
from dotenv import load_dotenv
import sqlite3
import random
import os
from pprint import pprint

from DB import db2

load_dotenv()

# reqsts_category = requests.get(f"https://developers.ria.com/auto/categories/?api_key={os.getenv('API_KEY')}").json()
# pprint(reqsts_category)

def chose_random_():
    """ Данная функция формирует список после ввода юзером настроек для вывода теста
        actual_dict_param отдает значения:
        1 - За посл неделю
        2 - За все время
        3 - рус --> англ
        4 - англ --> рус
    """

    actual_dict_param = []
    list_param_random = []

    for i in keyboard_choose()["inline_keyboard"]:
        for j in i:
            if j["text"][-1].startswith('✅'):
                print(["text"])
                actual_dict_param.append(j["callback_data"][-1])

    return actual_dict_param


# print(chose_random_())


def random_question(metod):

    connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
    cursor = connect.cursor()

    period_and_EN_or_RUS = chose_random_()

    if int(period_and_EN_or_RUS[0]) == int(1):
        # Делаем перебор из слов за НЕДЕЛЮ
        pass

    elif int(period_and_EN_or_RUS[0]) == int(2):
        # Делаем перебор из слов за ВСЕ ВРЕМЯ

        cursor.execute(f"""SELECT * FROM {metod}""")
        result = cursor.fetchall()

        random_data = random.choice(result)

        while True:
            random_data_2 = random.choice(result)

            if random_data_2[0] == random_data[0]:
                random_data_2 = random.choice(result)
                continue
            elif random_data_2[0] != random_data[0]:
                break





        return_list = [int(period_and_EN_or_RUS[1]), random_data, random_data_2]
        # [2, ('Яблоко', 'Apple', 'Thu Nov  3 14:03:26 2022'), ('3333', '44444', 'Thu Nov  3 14:56:17 2022')]

        return return_list


        # if period_and_EN_or_RUS[1] == int(3):
        #     # Отображаем слов на РУС
        #     random_data_rus = random_word

        #     return random_data_rus

        # elif int(period_and_EN_or_RUS[1]) == int(4):
        #     # Отображаем слов на АНГЛ
        #     random_data_eng = random_word

        #     return random_data_eng

# connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
# cursor = connect.cursor()
#
# metod = "phrase"
# cursor.execute(f"""SELECT * FROM {metod}""")
# result = cursor.fetchall()
#
# random_word = random.choice(result)
#
# print(random_word[0])

metod = "word"
(print(random_question(metod)))