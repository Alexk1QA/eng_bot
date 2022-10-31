from DB import db2
import sqlite3

def add_words(dict):

     car_models = db2.DB([f"words", "rus_name", "eng_name", "", ""])
     car_models.create_sm()
     car_models.insert_data(dict)

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