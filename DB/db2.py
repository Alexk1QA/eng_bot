from datetime import datetime, timedelta
from log.logging import logger_
import sqlite3
import json

# connect = sqlite3.connect("/Users/macbook/Desktop/english_bot_test/DB/eng_bot.accdb")
connect = sqlite3.connect("/home/ubuntu/eng_bot/DB/eng_bot.accdb")
cursor = connect.cursor()


class DB:
    def __init__(self, id_user: int):

        self.id_user = f"id_{id_user}"

    def create_table(self):
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.id_user}(
                                         id INTEGER PRIMARY KEY autoincrement,
                                         group_ TEXT,
                                         word_eng TEXT,
                                         word_rus TEXT,
                                         word_time_add timestamp,
                                         phrase_eng TEXT,
                                         phrase_rus TEXT,
                                         phrase_time_add timestamp,
                                         params_user TEXT,
                                         keyboard_boot int,
                                         temp_data TEXT,
                                         user_data TEXT
                                         )''')
        connect.commit()

# --------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------func for user_group--------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------#

    def actual_group(self) -> str:
        """
        @return: actual included group
        """
        cursor.execute(
            f""" SELECT params_user FROM {self.id_user} WHERE "id" = 1 """)
        user_group = json.loads(cursor.fetchall()[0][0])["user_group"]

        user_group_ = "Default"

        for i in user_group[f"dict_{user_group['status']}"].items():
            if i[1] == "✅":
                if i[0] == "All":
                    pass
                else:
                    user_group_ = i[0]

        return user_group_

    def update_group_up_to_default(self, del_groups: str = None, update_grp: str = None, old_grp: str = None) -> None:
        """
        @param del_groups: name to delete group
        @param update_grp: new name to update group
        @param old_grp: old name to update group
        @return: Nothing
        """

        if del_groups is not None:
            cursor.execute(f""" UPDATE {self.id_user} SET group_ = 'Default' WHERE group_ = '{del_groups}' """)
            connect.commit()

        if update_grp is not None:
            cursor.execute(f""" UPDATE {self.id_user} SET group_ = '{update_grp}' WHERE group_ = '{old_grp}' """)
            connect.commit()
# --------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------func for handlers----------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------#

    def insert_word_phrase(self, method: str, data_rus: str, data_eng: str) -> None:
        """
        @param method: column name part indicator
        @param data_rus: rus word
        @param data_eng: eng word
        @return: Nothing
        """

        cursor.execute(
            f"INSERT INTO {self.id_user} (group_, {f'{method}_rus'}, {f'{method}_eng'}, {f'{method}_time_add'})"
            f"VALUES ( ?, ?, ?, ?)", (self.actual_group(), data_rus, data_eng, datetime.now()))
        connect.commit()

    def insert_settings(self, params_user=None, status_=None, butt_dict=None, butt_dict_upd=None, user_data=None,
                        add_list_delete=None) -> None:

        if add_list_delete == "on":
            cursor.execute(
                f"INSERT INTO {self.id_user} ( user_data)"
                f"VALUES ( ? )", [user_data])
            connect.commit()
        else:
            list_ = [params_user, butt_dict, butt_dict_upd]

            count_ = 0

            for items in list_:
                if count_ == 0:
                    cursor.execute(
                        f"INSERT INTO {self.id_user} (params_user, keyboard_boot, user_data)"
                        f"VALUES ( ?, ? , ?)", (items, status_, user_data))
                    connect.commit()
                    count_ += 1

                else:
                    cursor.execute(
                        f"INSERT INTO {self.id_user} ( keyboard_boot)"
                        f"VALUES ( ? )", [items])
                    connect.commit()

# -------------------------------------------------   SELECT DATA  ---------------------------------------------------#

    def select_data_(self, column_: str = None, where_clmn: str = "id",
                     where_data: int = 1,  method_1: str = None,
                     method_2: str = None, word_during_period: str = None,
                     all_: str = None, pairs_all_or_one: str = None,
                     output_para: str = None, word_during_period_len: str = "off",
                     start_func: str = None,
                     custom_actual_group: str = None) -> [list, None]:

        actual_group_ = self.actual_group()

        if start_func == "on":
            actual_group_ = "All"

        if all_ == "on":

            if custom_actual_group is not None:
                cursor.execute(f"""SELECT {column_} FROM {self.id_user} WHERE {column_} is not Null 
                                                                        and group_ = '{custom_actual_group}' """)
                return cursor.fetchall()

            if actual_group_ == "All":
                cursor.execute(f""" SELECT {column_} FROM {self.id_user} WHERE {column_} is not Null""")
                return cursor.fetchall()

            else:
                cursor.execute(f"""SELECT {column_} FROM {self.id_user} WHERE {column_} is not Null 
                                                                        and group_ = '{actual_group_}' """)
                return cursor.fetchall()

        if pairs_all_or_one == "all" or pairs_all_or_one == "one":

            eng_data_ = f"{method_1}_eng"
            rus_data_ = f"{method_1}_rus"

            if pairs_all_or_one == "one":
                #  random one word pair

                if actual_group_ == "All":
                    cursor.execute(f""" SELECT {eng_data_} FROM {self.id_user} WHERE {eng_data_} is not null 
                                        ORDER BY RANDOM() LIMIT 1 """)
                    word_eng_ = cursor.fetchone()

                    cursor.execute(f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{word_eng_[0]}' """)
                    word_rus = cursor.fetchone()

                    return [word_eng_[0], word_rus[0]]

                else:
                    try:
                        cursor.execute(f""" SELECT {eng_data_} FROM {self.id_user} WHERE {eng_data_} is not null 
                                            and group_ = '{actual_group_}' ORDER BY RANDOM() LIMIT 1 """)
                        word_eng_ = cursor.fetchone()

                        cursor.execute(f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{word_eng_[0]}' 
                                                                                   and group_ = '{actual_group_}' """)
                        word_rus = cursor.fetchone()

                        return [word_eng_[0], word_rus[0]]
                    except Exception as ex:
                        logger_(self.id_user, f"file: handlers/delete_message_main /// {ex}")
                        return None

            elif pairs_all_or_one == "all":
                # all words
                all_list_data = []
                if actual_group_ == "All":

                    cursor.execute(f"""SELECT {eng_data_} FROM {self.id_user} WHERE {eng_data_} is not Null """)
                    list_word_eng_ = cursor.fetchall()

                    for eng_word in list_word_eng_:
                        cursor.execute(
                            f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{eng_word[0]}' """)
                        rus_word = cursor.fetchone()
                        all_list_data.append([eng_word[0], rus_word[0]])

                    return all_list_data

                else:
                    cursor.execute(f"""SELECT {eng_data_} FROM {self.id_user} WHERE {eng_data_} is not Null
                                                                              and group_ = '{actual_group_}'""")
                    list_word_eng_ = cursor.fetchall()

                    for eng_word in list_word_eng_:
                        cursor.execute(f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{eng_word[0]}' 
                                                                                   and group_ = '{actual_group_}' """)
                        rus_word = cursor.fetchone()
                        all_list_data.append([eng_word[0], rus_word[0]])

                    return all_list_data

        if word_during_period == "user_period":
            eng_data_ = f"{method_1}_eng"
            rus_data_ = f"{method_1}_rus"
            date_data = f"{method_1}_time_add"

            cursor.execute(f"""SELECT params_user FROM {self.id_user} WHERE id = 1 """)
            param_day_ = json.loads(cursor.fetchone()[0])["param_day"]

            if word_during_period_len == "on":

                if actual_group_ == "All":
                    cursor.execute(f""" SELECT {eng_data_} FROM {self.id_user} 
                                        WHERE {date_data} >= '{datetime.now() + timedelta(days=-param_day_ - 1)}'""")
                    return cursor.fetchall()

                else:
                    cursor.execute(f""" SELECT {eng_data_} FROM {self.id_user} 
                                        WHERE {date_data} >= '{datetime.now() + timedelta(days=-param_day_ - 1)}'
                                        and group_ = '{actual_group_}' """)
                    return cursor.fetchall()

            if actual_group_ == "All":
                cursor.execute(f""" SELECT {eng_data_} FROM {self.id_user} 
                                          WHERE {date_data} >= '{datetime.now() + timedelta(days=-param_day_ - 1)}' 
                                          ORDER BY RANDOM() LIMIT 1 """)
                word_eng_ = cursor.fetchone()

            else:
                cursor.execute(f""" SELECT {eng_data_} FROM {self.id_user} 
                                    WHERE {date_data} >= '{datetime.now() + timedelta(days=-param_day_ - 1)}' 
                                    and group_ = '{actual_group_}'
                                    ORDER BY RANDOM() LIMIT 1 """)
                word_eng_ = cursor.fetchone()

            if word_eng_ is None:
                return None

            else:
                if actual_group_ == "All":
                    cursor.execute(
                        f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{word_eng_[0]}' """)
                    word_rus = cursor.fetchone()

                    return [word_eng_[0], word_rus[0]]
                else:
                    cursor.execute(
                        f""" SELECT {rus_data_} FROM {self.id_user} WHERE {eng_data_} = '{word_eng_[0]}' 
                                                                    and group_ = '{actual_group_}'""")
                    word_rus = cursor.fetchone()

                    return [word_eng_[0], word_rus[0]]

        if column_ is not None:
            cursor.execute(f"""SELECT {column_} FROM {self.id_user} WHERE {where_clmn} = '{where_data}' """)
            return cursor.fetchall()

        if output_para == "on":
            column_eng = f"{method_1}_eng"
            column_rus = f"{method_1}_rus"

            where_clmn_ = f"{method_1}_{method_2}"

            # if actual_group_ == "All":
            cursor.execute(
                f"""SELECT {column_eng}, {column_rus}, group_ FROM {self.id_user} WHERE {where_clmn_} = '{where_data}' """)
            return cursor.fetchall()
            # else:
            #     cursor.execute(
            #         f"""SELECT {column_eng}, {column_rus} FROM {self.id_user} WHERE {where_clmn_} = '{where_data}'
            #                                                                   and group_ = '{actual_group_}'""")
            #     return cursor.fetchall()

# -------------------------------------------------   UPDATE DATA  ---------------------------------------------------#

    def update_data_(self, column_: str = None, where_clmn: str = "id",
                     where_data: int = 1, method_: str = None, data_updating: any = None) -> None:

        if method_ is not None:
            cursor.execute(f""" UPDATE {self.id_user} 
                                SET {f'word_{method_}'} = '{data_updating}' 
                                WHERE {f'word_{method_}'} = '{where_data}' """)
            connect.commit()

        else:
            cursor.execute(
                f""" UPDATE {self.id_user} SET '{column_}' = '{data_updating}' WHERE {where_clmn} = '{where_data}' """)
            connect.commit()

# -------------------------------------------------   DELETE DATA  ---------------------------------------------------#
    def delete_data(self, word: str) -> None:
        cursor.execute(f""" DELETE FROM {self.id_user} WHERE word_eng = '{word}' """)
        connect.commit()
