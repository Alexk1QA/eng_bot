import sqlite3
import time



# def data_base(wodr_rus, wodr_eng):
#
#     today_date = datetime.date.today()
#     new_today_date = today_date.strftime("%d-%m-%Y")
#
#     connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
#     cursor = connect.cursor()
#
#     cursor.execute(f'''CREATE TABLE IF NOT EXISTS words
#              (rus_name TEXT,
#               eng_name TEXT,
#               time_add TEXT
#               )''')
#     connect.commit()
#
#     cursor.execute(
#         f"INSERT INTO words (rus_name, eng_name, time_add)"
#         f"VALUES (?, ?, ?)", (wodr_rus, wodr_eng, new_today_date))
#     connect.commit()

connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
cursor = connect.cursor()



class DB:
    def __init__(self, metod):

        self.metod = metod

    def create_table(self):

        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.metod}(
                                 {f'{self.metod}_rus'} TEXT,
                                 {f'{self.metod}_eng'} TEXT,
                                 time_add TEXT
                                 )''')
        connect.commit()

    def insert_data(self, data_rus, data_eng):

        time_ = time.ctime()

        cursor.execute(
            f"INSERT INTO {self.metod} ({f'{self.metod}_rus'}, {f'{self.metod}_eng'}, time_add)"
            f"VALUES (?, ?, ?)", (data_rus, data_eng, time_))
        connect.commit()

    def select_data(self):
        cursor.execute(f"""SELECT * FROM {self.metod}""")

        result = cursor.fetchall()
        return result

    def delete_data(self):
        pass


    # def data_base(word_rus, wodr_eng):
    #     today_date = datetime.date.today()
    #     new_today_date = today_date.strftime("%d-%m-%Y")
    #
    #     connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
    #     cursor = connect.cursor()
    #
    #     cursor.execute(f'''CREATE TABLE IF NOT EXISTS words
    #              (rus_name TEXT,
    #               eng_name TEXT,
    #               time_add TEXT
    #               )''')
    #     connect.commit()
    #
    #     cursor.execute(
    #         f"INSERT INTO words (rus_name, eng_name, time_add)"
    #         f"VALUES (?, ?, ?)", (word_rus, wodr_eng, new_today_date))
    #     connect.commit()
    #





# wodr_rus = "Яблоко"
# wodr_eng = "Apple"
#
# data_base(wodr_rus,wodr_eng)
# #

# class DB:
#     def __init__(self, spisok):
#         self.spisok = spisok
#
#     def create_sm(self):
#         """Delete table s create new for inserting data"""
#         cursor.execute(f"""DROP TABLE IF EXISTS '{self.spisok[0]}'""")
#         connect.commit()
#
#         cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{self.spisok[0]}'(
#             '{self.spisok[1]}' char(256),
#             '{self.spisok[2]}'  char(256)
#
#         )""")
#         connect.commit()
#
#     def insert_data(self, items):
#         """Inserting data into table"""
#         cursor.execute(
#             f"INSERT INTO {self.spisok[0]} ({self.spisok[1]}, {self.spisok[2]})"
#             f"VALUES (?, ?)", (items["name"], items["value"]))
#         connect.commit()

    # def select_data(self, items):
    #     cursor.execute(f"""SELECT * FROM {self.spisok[0]}""")

