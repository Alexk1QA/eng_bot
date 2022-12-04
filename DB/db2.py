
from datetime import datetime, timedelta
import sqlite3

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
                                         param_questions int,
                                         param_percent int,
                                         status_ int,
                                         param_day int,
                                         param_answer int,
                                         temp_data TEXT,
                                         butt_dict_id int,
                                         butt_dict_data TEXT,
                                         butt_dict_upd_id int,
                                         butt_dict_upd_data TEXT
                                         )''')
        connect.commit()

# --------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------func for handlers----------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------#
    def insert_data(self, method, data_rus, data_eng):

        cursor.execute(
            f"INSERT INTO {self.id_user} ({f'{method}_rus'}, {f'{method}_eng'}, {f'{method}_time_add'})"
            f"VALUES ( ?, ?, ?)", (data_rus, data_eng, datetime.now()))
        connect.commit()

    def insert_settings(self, param_questions, param_percent, status_, param_day, param_answer, temp_data, butt_dict,
                        butt_dict_upd):

        cursor.execute(
          f"INSERT INTO {self.id_user} (param_questions, param_percent, status_, param_day, param_answer, temp_data)"
          f"VALUES ( ?, ?, ?, ?, ?, ?)", (param_questions, param_percent, status_, param_day, param_answer, temp_data))
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

# -------------------------------------------------   SELECT DATA  ---------------------------------------------------#
    def select_data_(self, column_=None, where_clmn="id", where_data=1, method_=None, word_during_period=None,
                     all_=None, pairs_all_or_one=None):

        if all_ == "on":
            cursor.execute(f"""SELECT {column_} FROM {self.id_user} WHERE {column_} is not Null """)
            return cursor.fetchall()

        if pairs_all_or_one == "all" or pairs_all_or_one == "one":

            eng_data_ = f"{method_}_eng"
            rus_data_ = f"{method_}_rus"

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

            eng_data_ = f"{method_}_eng"
            rus_data_ = f"{method_}_rus"
            date_data = f"{method_}_time_add"

            cursor.execute(f"""SELECT param_day FROM {self.id_user} WHERE id = 1 """)
            param_day_ = cursor.fetchone()[0]

            cursor.execute(
                f""" SELECT {eng_data_} 
                                   FROM {self.id_user} 
                                   WHERE {date_data} >= '{datetime.now() + timedelta(days=-param_day_-1)}' 
                                   ORDER BY RANDOM() LIMIT 1 """)
            word_eng_ = cursor.fetchone()

            cursor.execute(
                f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{word_eng_[0]}' """)
            word_rus = cursor.fetchone()

            return [word_eng_[0], word_rus[0]]

        if column_ is not None:
            cursor.execute(f"""SELECT {column_} FROM {self.id_user} WHERE {where_clmn} = '{where_data}' """)
            return cursor.fetchall()

# -------------------------------------------------   UPDATE DATA  ---------------------------------------------------#
    def update_data_(self, column_=None, where_clmn="id", where_data=1, method_=None, data_updating=None):

        if method_ is not None:
            cursor.execute(f""" UPDATE {self.id_user} 
                                        SET {f'word_{method_}'} = '{data_updating}' WHERE {f'word_{method_}'} = '{where_data}' """)
            return connect.commit()

        cursor.execute(f""" UPDATE {self.id_user} SET '{column_}' = '{data_updating}' WHERE {where_clmn} = '{where_data}' """)
        connect.commit()

# -------------------------------------------------   DELETE DATA  ---------------------------------------------------#
    def delete_data(self, word):
        cursor.execute(f""" DELETE FROM {self.id_user} WHERE word_eng = '{word}' """)
        connect.commit()

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
