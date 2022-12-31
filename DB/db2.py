from datetime import datetime, timedelta
import sqlite3
import json

# connect = sqlite3.connect("/Users/macbook/Desktop/english_bot_test/DB/eng_bot.accdb")
connect = sqlite3.connect("/home/ubuntu/eng_bot/DB/eng_bot.accdb")
cursor = connect.cursor()


class DB:
    def __init__(self, id_user):

        self.id_user = f"id_{id_user}"

    def create_table(self):
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.id_user}(
                                         id INTEGER PRIMARY KEY autoincrement,
                                         word_eng TEXT,
                                         word_rus TEXT,
                                         word_time_add timestamp,
                                         phrase_eng TEXT,
                                         phrase_rus TEXT,
                                         phrase_time_add timestamp,
                                         params_user TEXT,
                                         keyboard_boot int,
                                         temp_data TEXT
                                         )''')
        connect.commit()

# --------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------func for handlers----------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------#
    def insert_word_phrase(self, method, data_rus, data_eng):

        cursor.execute(
            f"INSERT INTO {self.id_user} ({f'{method}_rus'}, {f'{method}_eng'}, {f'{method}_time_add'})"
            f"VALUES ( ?, ?, ?)", (data_rus, data_eng, datetime.now()))
        connect.commit()

    def insert_settings(self, params_user, status_, butt_dict, butt_dict_upd):

        list_ = [params_user, butt_dict, butt_dict_upd]

        count_ = 0

        for items in list_:
            if count_ == 0:
                cursor.execute(
                    f"INSERT INTO {self.id_user} (params_user, keyboard_boot)"
                    f"VALUES ( ?, ? )", (items, status_))
                connect.commit()
                count_ += 1

            else:
                cursor.execute(
                    f"INSERT INTO {self.id_user} (keyboard_boot)"
                    f"VALUES ( ? )", [items])
                connect.commit()

# -------------------------------------------------   SELECT DATA  ---------------------------------------------------#
    def select_data_(self, column_=None, where_clmn="id", where_data=1, method_1=None, method_2=None,
                     word_during_period=None, all_=None, pairs_all_or_one=None, output_para=None):

        if all_ == "on":

            cursor.execute(f"""SELECT {column_} FROM {self.id_user} WHERE {column_} is not Null """)
            return cursor.fetchall()

        if pairs_all_or_one == "all" or pairs_all_or_one == "one":

            eng_data_ = f"{method_1}_eng"
            rus_data_ = f"{method_1}_rus"

            if pairs_all_or_one == "one":
                #  random one word pair
                cursor.execute(
                    f""" SELECT {eng_data_}
                                             FROM {self.id_user} 
                                             WHERE {eng_data_} is not null 
                                             ORDER BY RANDOM() LIMIT 1 """)
                word_eng_ = cursor.fetchone()

                cursor.execute(
                    f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{word_eng_[0]}' """)
                word_rus = cursor.fetchone()

                return [word_eng_[0], word_rus[0]]

            elif pairs_all_or_one == "all":
                # all words
                all_list_data = []

                cursor.execute(f"""SELECT {eng_data_} FROM {self.id_user} WHERE {eng_data_} is not Null """)
                list_word_eng_ = cursor.fetchall()

                for eng_word in list_word_eng_:
                    cursor.execute(
                        f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{eng_word[0]}' """)
                    rus_word = cursor.fetchone()

                    all_list_data.append([eng_word[0], rus_word[0]])

                return all_list_data

        if word_during_period == "user_period":
            eng_data_ = f"{method_1}_eng"
            rus_data_ = f"{method_1}_rus"
            date_data = f"{method_1}_time_add"

            cursor.execute(f"""SELECT params_user FROM {self.id_user} WHERE id = 1 """)
            param_day_ = json.loads(cursor.fetchone()[0])["param_day"]

            cursor.execute(
                f""" SELECT {eng_data_} 
                                   FROM {self.id_user} 
                                   WHERE {date_data} >= '{datetime.now() + timedelta(days=-param_day_ - 1)}' 
                                   ORDER BY RANDOM() LIMIT 1 """)
            word_eng_ = cursor.fetchone()

            cursor.execute(
                f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{word_eng_[0]}' """)
            word_rus = cursor.fetchone()

            return [word_eng_[0], word_rus[0]]

        if column_ is not None:
            cursor.execute(f"""SELECT {column_} FROM {self.id_user} WHERE {where_clmn} = '{where_data}' """)
            return cursor.fetchall()

        if output_para == "on":

            column_eng = f"{method_1}_eng"
            column_rus = f"{method_1}_rus"

            where_clmn_ = f"{method_1}_{method_2}"

            cursor.execute(f"""SELECT {column_eng}, {column_rus} FROM {self.id_user} WHERE {where_clmn_} = '{where_data}' """)
            return cursor.fetchall()

# -------------------------------------------------   UPDATE DATA  ---------------------------------------------------#
    def update_data_(self, column_=None, where_clmn="id", where_data=1, method_=None, data_updating=None):

        if method_ is not None:
            cursor.execute(f""" UPDATE {self.id_user} 
                                SET {f'word_{method_}'} = '{data_updating}' 
                                WHERE {f'word_{method_}'} = '{where_data}' """)
            return connect.commit()

        cursor.execute(
            f""" UPDATE {self.id_user} SET '{column_}' = '{data_updating}' WHERE {where_clmn} = '{where_data}' """)
        connect.commit()

# -------------------------------------------------   DELETE DATA  ---------------------------------------------------#
    def delete_data(self, word):
        cursor.execute(f""" DELETE FROM {self.id_user} WHERE word_eng = '{word}' """)
        connect.commit()
