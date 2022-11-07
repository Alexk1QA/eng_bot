import sqlite3
from pprint import pprint
from DB import db2

a = 2
print(a)

print(f'{"#" * 20} --- 1')

connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
cursor = connect.cursor()

param_questions = "param_questions"


word_rus = "word_rus"
word_eng = "word_eng"

cursor.execute(f"""SELECT {word_rus} FROM id_476610055""")
word_rus_list = cursor.fetchall()

cursor.execute(f"""SELECT {word_eng} FROM id_476610055""")
word_eng_list = cursor.fetchall()




dict_word = {}
list_word = []
a = [(None,), ('Яблоко',), ('Машина',), ('Тест',), ('Такси',), ('Фрукты',), ('Яблоко',), ('Голяк',), (None,), ('Яблоко',), (None,), (None,)]
b = [(None,), ('Apple',), ('Car',), ('Test',), ('Taxi',), ('Food',), ('Apple',), ('Brassic',), (None,), ('Apple',), (None,), (None,)]

# print(a)
# print(b)

for i in a:
        if i[0] is None:
            pass
        else:
            dict_word[f"{i[0]}"] = b[a.index(i)][0]
            list_word.append([i[0], b[a.index(i)][0]])

# print()
# pprint(dict_word)
# print(list_word)

create_table = db2.DB("id_476610055")
create_table.create_table()

param_percent = "param_percent"

w = int(create_table.select_data(param_percent)[0][0])

# print(w)

create_table.delete_data()


list_ = [[['Яблоко', 'Apple'], 'Apples'], [['Машина', 'Car'], 'Cor'], [['Нога', 'Leg'], 'Log']]



# for i in a:
#     para = i[0]
#     fail_word = i[1]
#     pass
#

def message_(list_):

    message_ = "\n"

    for i in list_:
        a = f"{i[0][0]} - {i[0][1]} - {i[1]}"
        message_ = f"{message_ + a} \n"

    return message_

# print(message_(list_))

test = 3
if int(test) == int(1) or int(test) == int(2):
    print("1 or 2")


id_ = 476610055

status_ = f"status_{id_}"
butt_dict = f"butt_dict_{id_}"
butt_dict_upd = f"butt_dict_upd_{id_}"


def individual_data_user(param):
    status = 1

    butt_dict = {
        "1": "За посл неделю ✅",
        "2": "За все время ",
        "3": "рус --> англ ✅",
        "4": "англ --> рус "
    }

    butt_dict_upd = {
        "1": "За посл неделю ",
        "2": "За все время ",
        "3": "рус --> англ ",
        "4": "англ --> рус "
    }

    if str(param) == "butt_dict":

        return butt_dict
    else:
        print("---")

param = "butt_dict"
print(individual_data_user(param))










# def random_question(metod, id):

#     # connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
#     # cursor = connect.cursor()

#     period_and_EN_or_RUS = chose_random_()

#     # period_and_EN_or_RUS = [2, 3]

#     if period_and_EN_or_RUS == None:
#         pass
#     else:
#         if int(period_and_EN_or_RUS[0]) == int(1):
#             # Делаем перебор из слов за НЕДЕЛЮ
#             pass

#         elif int(period_and_EN_or_RUS[0]) == int(2):
#             # Делаем перебор из слов за ВСЕ ВРЕМЯ
#             print("---")

#             word_rus_data_ = f"{metod}_rus"
#             word_eng_data_ = f"{metod}_eng"

#             create_table = db2.DB(f"{id}")
#             create_table.create_table()

#             word_rus_data = create_table.select_data(word_rus_data_)
#             word_eng_data = create_table.select_data(word_eng_data_)

#             list_data = []
#             # list_data --> [['Яблоко', 'Apple'], ['Машина', 'Car'], ['Дверь', 'Door']]

#             for i in word_rus_data:
#                 if i[0] is None:
#                     pass
#                 else:
#                     list_data.append([i[0], word_eng_data[word_rus_data.index(i)][0]])

#             random_data = random.choice(list_data)

#             return_list = [int(period_and_EN_or_RUS[1]), random_data]
#             return return_list
#             # return_list -->[3, [['Яблоко', 'Apple']]    