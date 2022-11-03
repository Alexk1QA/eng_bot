
import sqlite3
from pprint import pprint
import random
import  time
from DB import db2

def add_words(dict):



     car_models = db2.DB([f"words", "rus_name", "eng_name", "", ""])

     "/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb"



a = {'name': 'Яблоко', 'value': 'Apple'}

# add_words(a)

# connect = sqlite3.connect('eng_bot.accdb')
# cursor = connect.cursor()
#
# cursor.execute('''CREATE TABLE students
#          (eng_name TEXT,
#           rus_name TEXT,
#           name TEXT
#           )''')
# connect.commit()


# connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
# cursor = connect.cursor()

# cursor.execute(f"""SELECT * FROM words""")
# result = cursor.fetchall()
#
# aa = random.choice(result)

metod = "word"
phraze = "phrase"

# words = db2.DB(phraze)
# print(words.select_data())



butt_dict = {
        "1": "За посл неделю ",
        "2": "За все время ",
        "3": "рус --> англ ",
        "4": "англ --> рус"
}

butt_dict_2 = {
        "1": "За посл неделю ",
        "2": "За все время ✅",
        "3": "рус --> англ ",
        "4": "англ --> рус"
}

# print(butt_dict["2"])

# print(butt_dict["2"][-3])


def update_dict(button, dict_):

     done = "✅"
     butt_dict_1_1 = {}

     for i in dict_.items():
          print(i)
          # match int(i[0]):
          if int(i[0]) == int(button):
               # case int(buttton):

               match i[1][-1]:
                    case " ":
                         butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
                    case "✅":
                         butt_dict_1_1.update({f"{i[0]}": f"{i[1]} "})
          else:
               butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})
     print(butt_dict_1_1)
     print("1")
     return butt_dict_1_1         

button = "1"

# print(update_dict(button, butt_dict))


# print(butt_dict["2"][-1])
# print(update_dict(butt_dict["1"][-1]), butt_dict)


def update_dict_2(button, dict_):

     done = "✅"
     butt_dict_1_1 = {}

     for i in dict_.items():
          print(i)
          # match int(i[0]):
          if int(i[0]) == int(button):
               # case int(buttton):

               match i[1][-1]:
                    case " ":
                         butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
                    case "✅":
                         butt_dict_1_1.update({f"{i[0]}": f"{i[0:-1]} "})
          else:
               butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})
     return butt_dict_1_1         


# print(update_dict_2(button, update_dict(button, butt_dict)))





# d = time.ctime()

# print(d)



# def new_func_procents():

#      cortezh = [('Яблоко', 'Apple', 'Thu Nov  3 13:18:53 2022'),
#       ('qeweqwewqewqewqewqeqwe', 'wqewqeqre23432432423423',
#        'Thu Nov  3 13:57:55 2022'), ('1', '2', 'Thu Nov  3 13:58:32 2022'),
#         ('qqq', 'wwww', 'Thu Nov  3 14:06:47 2022')]


#       random_word = random.choice(result)



param_fails = 47


question = 10

answer = 4


