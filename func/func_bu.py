from keyboard.keyboard_bu_inline import *
from DB import db2


def message_(list_: [list, dict], word_: str = None, only_active_group: str = None,
             len_word_in_groups: str = None, user_id: int = None) -> str:
    """ Function for generating a list message with incorrect words """
    # Input example: - [['d2', 'd'], 'ee']] /// ['d2', 'd'] - pair word from DB /// 'ee' - answered our user

    if type(list_) == dict:

        message_out = "\n\n"
        count_word = 1

        data_base = db2.DB(user_id)

        for i in list_.items():

            if only_active_group == "on":
                if i[1] == "✅":
                    return f"{i[0]}"
            else:

                if len_word_in_groups == "on":
                    print(i[0])
                    if i[0] == "All":
                        pass
                    else:
                        len_group = len(data_base.select_data_(column_="word_eng", all_="on", custom_actual_group=i[0]))
                        a = f"{count_word} - {i[0]} {len_group}"
                        message_out = f"{message_out + a} \n"
                        count_word += 1

                else:
                    a = f"{count_word} - {i[0]} {i[1]}"
                    message_out = f"{message_out + a} \n"
                    count_word += 1

        return message_out

    else:
        if type(list_[0]) == tuple:

            message_out = f"\n\n"
            count_word = 1

            for i in list_:
                a = f"{count_word} - Группа : {i[2]} - {i[0]} / {i[1]}"
                message_out = f"{message_out + a} \n"
                count_word += 1
            space = "\n"
            message_out = f"""{message_out + f"{space}Вы добавляете {word_}"}"""
            return message_out

        elif type(list_[0][0]) == list:
            message_out = "\n\n"
            count_word = 1

            for i in list_:
                a = f"{count_word} - {i[0][0]} / {i[0][1]}. Вы ввели - «{i[1]}»"
                message_out = f"{message_out + a} \n"
                count_word += 1

            return message_out

        else:
            message_out = "\n\n"
            count_word = 1

            for i in list_:
                a = f"{count_word} - {i} / {i}. Вы ввели - «{i[1]}»"
                message_out = f"{message_out + a} \n"
                count_word += 1

            return message_out


def chose_random_(user_id: int) -> list:
    """ This function generates a list after the user enters the settings for the test output
        actual_dict_param gives the values:
        1 - user period, 2 - all time, 3 - rus --> eng, 4 - eng --> rus """

    actual_dict_param = []

    for i in keyboard_choose(user_id)["inline_keyboard"]:
        for j in i:
            if j["text"].count('✅') == 1:
                actual_dict_param.append(j["callback_data"][-1])

    return actual_dict_param


def random_question(method_: str, user_id: int, mode_func: str = None):
    # Input example: "word", message.from_user.id, 0

    period_and_EN_or_RUS = chose_random_(user_id)
    # example period_and_EN_or_RUS --> [2, 3]

    if period_and_EN_or_RUS is None or len(period_and_EN_or_RUS) < 2:
        return None

    else:

        call_back_period = period_and_EN_or_RUS[0]

        data_base = db2.DB(user_id)

        if mode_func == "download":
            random_from_all = data_base.select_data_(method_1=method_, pairs_all_or_one="all")
            # with open(f'/Users/macbook/Desktop/english_bot_test/temporary/words_id_{user_id}.txt', 'w') as file:
            with open(f'/home/ubuntu/eng_bot/temporary/words_id_{user_id}.txt', 'w') as file:

                return file.writelines(f'{row[1]} - {row[0]}\n' for row in random_from_all)

        else:
            if int(period_and_EN_or_RUS[0]) == int(1):

                random_from_user_period = data_base.select_data_(method_1=method_, word_during_period="user_period")

                if random_from_user_period is None:
                    return None
                else:
                    return [int(period_and_EN_or_RUS[1]), random_from_user_period, call_back_period]
                # Output: [3, [['Яблоко', 'Apple'], 1]

            elif int(period_and_EN_or_RUS[0]) == int(2):

                random_from_all = data_base.select_data_(method_1=method_, pairs_all_or_one="one")
                if random_from_all is None:
                    return None
                else:
                    return [int(period_and_EN_or_RUS[1]), random_from_all, call_back_period]
                    # Output: [3, [['Яблоко', 'Apple'], 1]


def check_word_phrase_replay(mode, user_id: int, list_asked_data: list,
                             len_data_alltime: int, len_data_week: int) -> [list, None]:
    max_count = 0

    while True:
        data_ = random_question(mode, user_id)

        if max_count == 500:
            return data_

        if data_ is None:
            return None

        len_data_ = 0

        if int(data_[2]) == 1:
            len_data_ = len_data_week

        elif int(data_[2]) == 2:
            len_data_ = len_data_alltime

        if len_data_ == len(list_asked_data):
            list_asked_data.clear()
            break

        if data_[1][0] in list_asked_data:
            pass
        else:
            break
        max_count += 1

    return data_


def middle_percent_(user_id: int, new_percents: int = None, mode: str = ""):

    data_base = db2.DB(user_id)

    try:
        if mode == "":
            raise

        params_user = json.loads(data_base.select_data_(column_="params_user", where_clmn="id",
                                                                where_data=1)[0][0])

        if mode == "read":

            return params_user["middle_percent"][0] / params_user["middle_percent"][1]

        elif mode == "write":
            params_user["middle_percent"] = [params_user["middle_percent"][0] + new_percents,
                                             params_user["middle_percent"][1] + 1]

            data_base.update_data_(column_="params_user", data_updating=json.dumps(params_user))

    except Exception as ex:
        return {"error": f"arg mode is not 'read' or 'write' /// Exception: {ex}"}

