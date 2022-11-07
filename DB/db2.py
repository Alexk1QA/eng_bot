import sqlite3
import time

connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
cursor = connect.cursor()



class DB:
    def __init__(self, id):

        self.id = id

    def create_table(self):

        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.id}(
                                         id INTEGER PRIMARY KEY autoincrement,
                                         word_rus TEXT,
                                         word_eng TEXT,
                                         word_time_add timestamp,
                                         phrase_rus TEXT,
                                         phrase_eng TEXT,
                                         phrase_time_add timestamp,
                                         param_questions TEXT,
                                         param_percent TEXT
                                         )''')
        connect.commit()

    def insert_data(self, metod, data_rus, data_eng):

        time_ = time.ctime()

        cursor.execute(
            f"INSERT INTO {self.id} ({f'{metod}_rus'}, {f'{metod}_eng'}, {f'{metod}_time_add'})"
            f"VALUES ( ?, ?, ?)", (data_rus, data_eng, time_))
        connect.commit()

    def insert_settings(self, param_questions, param_percent):

        cursor.execute(
            f"INSERT INTO {self.id} (param_questions, param_percent)"
            f"VALUES ( ?, ?)", (param_questions, param_percent))
        connect.commit()

    def select_data(self, column_):
        cursor.execute(f"""SELECT {column_} FROM {self.id}""")

        result = cursor.fetchall()
        return result

    def update_data(self):
        pass

    def delete_data(self):
        print("")




# class DB:
#     def __init__(self, id):
#
#         self.id = id
#
#     def create_table(self):
#
#         cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.id}(
#                                          id INTEGER PRIMARY KEY autoincrement,
#                                          word_rus TEXT,
#                                          word_eng TEXT,
#                                          word_time_add TEXT,
#                                          phrase_rus TEXT,
#                                          phrase_eng TEXT,
#                                          phrase_time_add TEXT,
#                                          param_questions TEXT,
#                                          param_percent TEXT
#                                          )''')
#         connect.commit()
#
#     def insert_data(self, metod, data_rus, data_eng):
#
#         time_ = time.ctime()
#
#         cursor.execute(
#             f"INSERT INTO {self.id} ({f'{metod}_rus'}, {f'{metod}_eng'}, {f'{metod}_time_add'})"
#             f"VALUES ( ?, ?, ?)", (data_rus, data_eng, time_))
#         connect.commit()
#
#     def insert_settings(self, param_questions, param_percent):
#
#         cursor.execute(
#             f"INSERT INTO {self.id} (param_questions, param_percent)"
#             f"VALUES ( ?, ?)", (param_questions, param_percent))
#         connect.commit()
#
#     def select_data(self, column_):
#         cursor.execute(f"""SELECT {column_} FROM {self.id}""")
#
#         result = cursor.fetchall()
#         return result
#
#     def update_data(self):
#         pass
#
#     def delete_data(self):
#         print("")