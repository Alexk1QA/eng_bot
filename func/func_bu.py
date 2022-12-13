from keyboard.keyboard_bu_inline import *
from DB import db2


def message_(list_, word_=None):
    """ Function for generating a list message with incorrect words """
    # Input example: - [['d2', 'd'], 'ee']] /// ['d2', 'd'] - pair word from DB /// 'ee' - answered our user

    if type(list_[0]) == tuple:

        message_out = f"\n\n"
        count_word = 1

        for i in list_:
            a = f"{count_word} - {i[0]} / {i[1]}"
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


def chose_random_(user_id):
    """ This function generates a list after the user enters the settings for the test output
        actual_dict_param gives the values:
        1 - last week, 2 - all time, 3 - rus --> eng, 4 - eng --> rus """

    actual_dict_param = []

    for i in keyboard_choose(user_id)["inline_keyboard"]:
        for j in i:
            if j["text"][-1].startswith('✅') or j["text"][-8].startswith('✅'):
                actual_dict_param.append(j["callback_data"][-1])

    return actual_dict_param


def random_question(method_, user_id, mode_func=None):
    # Input example: "word", message.from_user.id, 0

    period_and_EN_or_RUS = chose_random_(user_id)
    # example period_and_EN_or_RUS --> [2, 3]

    if period_and_EN_or_RUS is None or len(period_and_EN_or_RUS) < 2:

        return None

    else:
        data_base = db2.DB(user_id)

        if mode_func == "download":
            random_from_all = data_base.select_data_(method_=method_, pairs_all_or_one="all")
            # with open(f'/Users/macbook/Desktop/english_bot_test/temporary/words_id_{user_id}.txt', 'w') as file:
            with open(f'/home/ubuntu/eng_bot/temporary/words_id_{user_id}.txt', 'w') as file:

                return file.writelines(f'{row[1]} - {row[0]}\n' for row in random_from_all)

        else:
            if int(period_and_EN_or_RUS[0]) == int(1):

                random_from_user_period = data_base.select_data_(method_1=method_, word_during_period="user_period")

                return [int(period_and_EN_or_RUS[1]), random_from_user_period]
                # Output: [3, [['Яблоко', 'Apple']]

            elif int(period_and_EN_or_RUS[0]) == int(2):

                random_from_all = data_base.select_data_(method_1=method_, pairs_all_or_one="one")
                return [int(period_and_EN_or_RUS[1]), random_from_all]
                # Output: [3, [['Яблоко', 'Apple']]
