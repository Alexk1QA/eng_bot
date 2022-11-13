from datetime import datetime
import sqlite3

# connect = sqlite3.connect("/Users/macbook/Desktop/english_bot/DB/eng_bot.accdb")
connect = sqlite3.connect("/home/ubuntu/eng_bot_2/eng_bot/DB/eng_bot.accdb")
cursor = connect.cursor()


class DB:
    def __init__(self, id_user):

        self.id_user = f"id_{id_user}"

    def create_table(self):
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.id_user}(
                                         id INTEGER PRIMARY KEY autoincrement,
                                         word_rus TEXT,
                                         word_eng TEXT,
                                         word_time_add timestamp,
                                         phrase_rus TEXT,
                                         phrase_eng TEXT,
                                         phrase_time_add timestamp,
                                         param_questions int,
                                         param_percent int,
                                         status_ int,
                                         param_day int,
                                         butt_dict_id int,
                                         butt_dict_data TEXT,
                                         butt_dict_upd_id int,
                                         butt_dict_upd_data TEXT
                                         
                                         )''')
        connect.commit()

# --------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------func for handlers----------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------#
    def insert_data(self, metod, data_rus, data_eng):

        time_ = datetime.now().strftime("%d-%m-%y  %H:%M:%S")

        cursor.execute(
            f"INSERT INTO {self.id_user} ({f'{metod}_rus'}, {f'{metod}_eng'}, {f'{metod}_time_add'})"
            f"VALUES ( ?, ?, ?)", (data_rus, data_eng, time_))
        connect.commit()

    def insert_settings(self, param_questions, param_percent, status_, param_day, butt_dict, butt_dict_upd):

        cursor.execute(
            f"INSERT INTO {self.id_user} (param_questions, param_percent, status_, param_day)"
            f"VALUES ( ?, ?, ?, ?)", (param_questions, param_percent, status_, param_day))
        connect.commit()

        for i in butt_dict.items():
            cursor.execute(
                f"INSERT INTO {self.id_user} (butt_dict_id, butt_dict_data)"
                f"VALUES ( ?, ? )", (i[0], i[1]))
            connect.commit()

        for i in butt_dict_upd.items():
            cursor.execute(
                f"INSERT INTO {self.id_user} (butt_dict_upd_id, butt_dict_upd_data)"
                f"VALUES ( ?, ? )", (i[0], i[1]))
            connect.commit()

    def settings_update(self, column_, data_updating):
        cursor.execute(f""" UPDATE {self.id_user} SET '{column_}' = '{data_updating}' WHERE id = 1 """)
        connect.commit()

    def select_data(self, column_):
        # cursor.execute(f"""SELECT {column_} FROM {self.id_user}""")

        cursor.execute(f"""SELECT {column_} FROM {self.id_user} WHERE {column_} is not Null """)

        result = cursor.fetchall()
        return result

# --------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------func for inline keyboard------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------#
    def status_update(self, data_updating):
        cursor.execute(f""" UPDATE {self.id_user} SET status_ = '{data_updating}' WHERE id = 1 """)
        connect.commit()

    def butt_dict_update(self, data_updating):

        for i in data_updating.items():
            cursor.execute(f""" UPDATE {self.id_user} SET butt_dict_data = '{i[1]}' 
                                                      WHERE butt_dict_id = '{int(i[0])}' """)
            connect.commit()

    def butt_dict_upd_update(self, data_updating):
        for i in data_updating.items():
            cursor.execute(f""" UPDATE {self.id_user} SET butt_dict_upd_data = '{i[1]}' 
                                                      WHERE butt_dict_upd_id = '{int(i[0])}' """)
            connect.commit()

    def status_select(self):
        cursor.execute(f"""SELECT status_ FROM {self.id_user} WHERE status_ is not Null """)
        status_ = cursor.fetchall()
        return status_

    def butt_dict_select(self):

        cursor.execute(f"""SELECT butt_dict_id FROM {self.id_user} WHERE butt_dict_id is not Null """)
        butt_dict_id = cursor.fetchall()

        cursor.execute(f"""SELECT butt_dict_data FROM {self.id_user} WHERE butt_dict_data is not Null """)
        butt_dict_data = cursor.fetchall()

        butt_dict = {}

        for i in butt_dict_id:
                butt_dict[f"{i[0]}"] = f"{butt_dict_data[butt_dict_id.index(i)][0]}"

        return butt_dict

    def butt_dict_upd_select(self):

        cursor.execute(f"""SELECT butt_dict_upd_id FROM {self.id_user} WHERE butt_dict_upd_id is not Null """)
        butt_dict_id = cursor.fetchall()

        cursor.execute(f"""SELECT butt_dict_upd_data FROM {self.id_user} WHERE butt_dict_upd_data is not Null """)
        butt_dict_data = cursor.fetchall()

        butt_dict_upd = {}

        for i in butt_dict_id:
                butt_dict_upd[f"{i[0]}"] = f"{butt_dict_data[butt_dict_id.index(i)][0]}"

        return butt_dict_upd

# --------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------------func in development------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------#

    def update_data_for_user(self):
        pass

    def delete_data(self):
        pass