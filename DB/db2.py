import sqlite3



def data_base(wodr_rus, wodr_eng):
    connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
    cursor = connect.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS words
             (rus_name TEXT,
              eng_name TEXT,
              name TEXT
              )''')
    connect.commit()

    cursor.execute(
        f"INSERT INTO words (rus_name, eng_name)"
        f"VALUES (?, ?)", (wodr_rus, wodr_eng))
    connect.commit()

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
    #     result =
