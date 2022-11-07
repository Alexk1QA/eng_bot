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