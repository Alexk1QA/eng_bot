from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

button_test_1 = KeyboardButton("Test")
keyboard_Test_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_test_1)

button_Choose_Continue = KeyboardButton("Продолжить")
keyboard_Choose_Continue = ReplyKeyboardMarkup(resize_keyboard=True).add(button_Choose_Continue)


# def individual_data_user(param_data, param_mode, update_data):
#
#     status = 1
#
#     butt_dict = {
#             "1": "За посл неделю ✅",
#             "2": "За все время ",
#             "3": "рус --> англ ✅",
#             "4": "англ --> рус "
#     }
#
#     butt_dict_upd = {
#              "1": "За посл неделю ",
#              "2": "За все время ",
#              "3": "рус --> англ ",
#              "4": "англ --> рус "
#     }
#
#     match str(param_mode):
#
#         case "read":
#             match str(param_data):
#                 case "status":
#                     return status
#                 case "butt_dict":
#                     return butt_dict
#                 case "butt_dict_upd":
#                     return butt_dict_upd
#
#         case "write":
#             match str(param_data):
#                 case "status":
#                     status = update_data
#                 case "butt_dict":
#                     butt_dict = update_data
#                 case "butt_dict_upd":
#                     butt_dict_upd = update_data
#
#
# def update_keyboard_secondary(button, dict_):
#     """ Доп функция для динамического изменения инлайн кнопок
#        Тут мы перезаписываем второй словарь """
#
#     # global butt_dict_upd, status, butt_dict
#
#     print("############### update_keyboard_secondary")
#
#     done = "✅"
#     butt_dict_1_1 = {}
#
#     for i in dict_.items():
#         if int(i[0]) == int(button):
#             match i[1][-1]:
#                 case " ":
#                         butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
#                 case "✅":
#                         butt_dict_1_1.update({f"{i[0]}": f"{i[1][0:-1]} "})
#         else:
#             butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})
#
#     match int(button):
#
#         case int(1):
#             butt_dict_1_1.update({"2": "За все время "})
#
#         case int(2):
#             butt_dict_1_1.update({"1": "За посл неделю "})
#
#         case int(3):
#             butt_dict_1_1.update({"4": "англ --> рус "})
#
#         case int(4):
#             butt_dict_1_1.update({"3": "рус --> англ "})
#
#     param_mode = "read"
#     update_data = None
#     param_data = "status"
#     status = individual_data_user(param_data, param_mode, update_data)
#
#     if status == 1:
#         print(f"update_keyboard_secondary - status == 1")
#
#         param_mode = "write"
#         update_data = butt_dict_1_1
#         param_data = "butt_dict_upd"
#         individual_data_user(param_data, param_mode, update_data)
#
#         print(butt_dict_1_1)
#         return butt_dict_1_1
#
#     elif status == 0:
#         print(f"update_keyboard_secondary - status == 0")
#
#         param_mode = "write"
#         update_data = butt_dict_1_1
#         param_data = "butt_dict"
#         individual_data_user(param_data, param_mode, update_data)
#
#         return butt_dict_1_1
#
#
# def update_keyboard_main(button):
#     """Доп функция для динамического изменения инлайн кнопок"""
#
#     # global status
#
#     print("############### update_keyboard_main")
#
#     param_mode = "read"
#     update_data = None
#
#     param_data = "butt_dict"
#     butt_dict = individual_data_user(param_data, param_mode, update_data)
#     print(f"update_keyboard_main - butt_dict {butt_dict}")
#
#     param_data = "butt_dict_upd"
#     butt_dict_upd = individual_data_user(param_data, param_mode, update_data)
#     print(f"update_keyboard_main - butt_dict_upd {butt_dict_upd}")
#
#     param_data = "status"
#     status = individual_data_user(param_data, param_mode, update_data)
#     print(f"update_keyboard_main - status {status}")
#
#     if status == 1:
#         actual_dict = update_keyboard_secondary(button, butt_dict)
#
#         param_mode = "write"
#         update_data = 0
#         param_data = "status"
#         individual_data_user(param_data, param_mode, update_data)
#
#         a = 1
#         if a == 1:
#             param_mode = "read"
#             update_data = None
#
#             param_data = "butt_dict_upd"
#             butt_dict = individual_data_user(param_data, param_mode, update_data)
#
#             print(f"update_keyboard_main a == 1 {butt_dict}")
#
#         return actual_dict
#
#     elif status == 0:
#         actual_dict = update_keyboard_secondary(button, butt_dict_upd)
#
#         param_mode = "write"
#         update_data = 1
#         param_data = "status"
#         individual_data_user(param_data, param_mode, update_data)
#
#         print(f"update_keyboard_main {actual_dict}")
#
#         return actual_dict
#
#
# def keyboard_choose():
#     """Функция для динамического изменения инлайн кнопок в ручном режиме выбора параметров"""
#
#     # global inline_keyboard_choose, status
#
#     print("############### keyboard_choose")
#
#     param_mode = "read"
#     update_data = None
#
#     param_data = "butt_dict"
#     butt_dict = individual_data_user(param_data, param_mode, update_data)
#     print(f"keyboard_choose - butt_dict {butt_dict}")
#
#     param_data = "butt_dict_upd"
#     butt_dict_upd = individual_data_user(param_data, param_mode, update_data)
#     print(f"keyboard_choose - butt_dict_upd {butt_dict_upd}")
#
#     param_data = "status"
#     status = individual_data_user(param_data, param_mode, update_data)
#     print(f"keyboard_choose - status {status}")
#
#     if status == 1:
#         inline_button_1 = InlineKeyboardButton(text=f"{butt_dict['1']}", callback_data=f"inline_button_1")
#         inline_button_2 = InlineKeyboardButton(text=f"{butt_dict['2']}", callback_data=f"inline_button_2")
#         inline_button_3 = InlineKeyboardButton(text=f"{butt_dict['3']}", callback_data=f"inline_button_3")
#         inline_button_4 = InlineKeyboardButton(text=f"{butt_dict['4']}", callback_data=f"inline_button_4")
#
#         inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
#                                                                        inline_button_3, inline_button_4)
#         return inline_keyboard_choose
#
#     elif status == 0:
#         inline_button_1 = InlineKeyboardButton(text=f"{butt_dict_upd['1']}", callback_data=f"inline_button_1")
#         inline_button_2 = InlineKeyboardButton(text=f"{butt_dict_upd['2']}", callback_data=f"inline_button_2")
#         inline_button_3 = InlineKeyboardButton(text=f"{butt_dict_upd['3']}", callback_data=f"inline_button_3")
#         inline_button_4 = InlineKeyboardButton(text=f"{butt_dict_upd['4']}", callback_data=f"inline_button_4")
#
#
#         inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
#                                                                        inline_button_3, inline_button_4)
#         return inline_keyboard_choose










# status = 1
# butt_dict = {
#         "1": "За посл неделю ✅",
#         "2": "За все время ",
#         "3": "рус --> англ ✅",
#         "4": "англ --> рус "
# }
# 
# butt_dict_upd = {
#          "1": "За посл неделю ",
#          "2": "За все время ",
#          "3": "рус --> англ ",
#          "4": "англ --> рус "
# }
# 
# 
# def update_keyboard_secondary(button, dict_):
#     """ Доп функция для динамического изменения инлайн кнопок
#        Тут мы перезаписываем второй словарь """
# 
#     global butt_dict_upd, status, butt_dict
# 
#     done = "✅"
#     butt_dict_1_1 = {}
# 
#     for i in dict_.items():
#         if int(i[0]) == int(button):
#             match i[1][-1]:
#                 case " ":
#                         butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
#                 case "✅":
#                         butt_dict_1_1.update({f"{i[0]}": f"{i[1][0:-1]} "})
#         else:
#             butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})
# 
#     match int(button):
# 
#         case int(1):
#             butt_dict_1_1.update({"2": "За все время "})
# 
#         case int(2):
#             butt_dict_1_1.update({"1": "За посл неделю "})
# 
#         case int(3):
#             butt_dict_1_1.update({"4": "англ --> рус "})
# 
#         case int(4):
#             butt_dict_1_1.update({"3": "рус --> англ "})
# 
#     if status == 1:
#         butt_dict_upd = butt_dict_1_1
#         return butt_dict_upd
#     elif status == 0:
#         butt_dict = butt_dict_1_1
#         return butt_dict
# 
# 
# def update_keyboard_main(button):
#     """Доп функция для динамического изменения инлайн кнопок"""
# 
#     global status
# 
#     if status == 1:
#         actual_dict = update_keyboard_secondary(button, butt_dict)
#         status = 0
#         return actual_dict
#     elif status == 0:
#         actual_dict = update_keyboard_secondary(button, butt_dict_upd)
#         status = 1
#         return actual_dict
# 
# 
# def keyboard_choose():
#     """Функция для динамического изменения инлайн кнопок в ручном режиме выбора параметров"""
#     global inline_keyboard_choose, status
# 
#     if status == 1:
#         inline_button_1 = InlineKeyboardButton(text=f"{butt_dict['1']}", callback_data=f"inline_button_1")
#         inline_button_2 = InlineKeyboardButton(text=f"{butt_dict['2']}", callback_data=f"inline_button_2")
#         inline_button_3 = InlineKeyboardButton(text=f"{butt_dict['3']}", callback_data=f"inline_button_3")
#         inline_button_4 = InlineKeyboardButton(text=f"{butt_dict['4']}", callback_data=f"inline_button_4")
# 
#         inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
#                                                                        inline_button_3, inline_button_4)
#         return inline_keyboard_choose
# 
#     elif status == 0:
#         inline_button_1 = InlineKeyboardButton(text=f"{butt_dict_upd['1']}", callback_data=f"inline_button_1")
#         inline_button_2 = InlineKeyboardButton(text=f"{butt_dict_upd['2']}", callback_data=f"inline_button_2")
#         inline_button_3 = InlineKeyboardButton(text=f"{butt_dict_upd['3']}", callback_data=f"inline_button_3")
#         inline_button_4 = InlineKeyboardButton(text=f"{butt_dict_upd['4']}", callback_data=f"inline_button_4")
# 
# 
#         inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
#                                                                        inline_button_3, inline_button_4)
#         return inline_keyboard_choose







# ################## Попытка реализовать классы в клавиатуре ################## 

global butt_dict_upd, status, butt_dict, butt_dict_1_1


class INLINE_KEYBOARD:

    # butt_dict = {
    #     "1": "За посл неделю ✅",
    #     "2": "За все время ",
    #     "3": "рус --> англ ✅",
    #     "4": "англ --> рус "
    # }
    #
    # butt_dict_upd = {
    #     "1": "За посл неделю ",
    #     "2": "За все время ",
    #     "3": "рус --> англ ",
    #     "4": "англ --> рус "
    # }
    #
    # butt_dict_1_1 = {}
    #
    # status = 1

    def __init__(self, id):

        butt_dict = {
            "1": "За посл неделю ✅",
            "2": "За все время ",
            "3": "рус --> англ ✅",
            "4": "англ --> рус "
        }

        butt_dict_upd = {
            "1": "За посл неделю ",
            "2": "За все время ",
            "3": "рус --> англ ",
            "4": "англ --> рус "
        }

        butt_dict_1_1 = {}

        status = 1

        self.id = id
        self.status = status

        self.butt_dict = butt_dict
        self.butt_dict_upd = butt_dict_upd
        self.butt_dict_1_1 = butt_dict_1_1

    def update_keyboard_secondary(self, button, dict_):
        """ Доп функция для динамического изменения инлайн кнопок
        Тут мы перезаписываем второй словарь """

        done = "✅"
        self.butt_dict_1_1 = {}

        for i in dict_.items():
            if int(i[0]) == int(button):
                match i[1][-1]:
                    case " ":
                        self.butt_dict_1_1.update({f"{i[0]}": f"{i[1]}{done}"})
                    case "✅":
                        self.butt_dict_1_1.update({f"{i[0]}": f"{i[1][0:-1]} "})
            else:
                self.butt_dict_1_1.update({f"{i[0]}": f"{i[1]}"})

        match int(button):

            case int(1):
                self.butt_dict_1_1.update({"2": "За все время "})

            case int(2):
                self.butt_dict_1_1.update({"1": "За посл неделю "})

            case int(3):
                self.butt_dict_1_1.update({"4": "англ --> рус "})

            case int(4):
                self.butt_dict_1_1.update({"3": "рус --> англ "})

        if self.status == 1:
            self.butt_dict_upd = self.butt_dict_1_1
            return self.butt_dict_upd
        elif self.status == 0:
            self.butt_dict = self.butt_dict_1_1
            return self.butt_dict

    def update_keyboard_main(self, button):
        """Доп функция для динамического изменения инлайн кнопок"""

        if self.status == 1:
            actual_dict = self.update_keyboard_secondary(button, self.butt_dict)

            self.status = 0
            return self.keyboard_choose()

        elif self.status == 0:
            actual_dict = self.update_keyboard_secondary(button, butt_dict_upd)
            self.status = 1
            return actual_dict

    def keyboard_choose(self):
        """Функция для динамического изменения инлайн кнопок в ручном режиме выбора параметров"""
        # global inline_keyboard_choose, status

        if self.status == 1:
            inline_button_1 = InlineKeyboardButton(text=f"{self.butt_dict['1']}", callback_data=f"inline_button_1")
            inline_button_2 = InlineKeyboardButton(text=f"{self.butt_dict['2']}", callback_data=f"inline_button_2")
            inline_button_3 = InlineKeyboardButton(text=f"{self.butt_dict['3']}", callback_data=f"inline_button_3")
            inline_button_4 = InlineKeyboardButton(text=f"{self.butt_dict['4']}", callback_data=f"inline_button_4")

            inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                           inline_button_3, inline_button_4)
            return inline_keyboard_choose

        elif self.status == 0:
            inline_button_1 = InlineKeyboardButton(text=f"{self.butt_dict_upd['1']}", callback_data=f"inline_button_1")
            inline_button_2 = InlineKeyboardButton(text=f"{self.butt_dict_upd['2']}", callback_data=f"inline_button_2")
            inline_button_3 = InlineKeyboardButton(text=f"{self.butt_dict_upd['3']}", callback_data=f"inline_button_3")
            inline_button_4 = InlineKeyboardButton(text=f"{self.butt_dict_upd['4']}", callback_data=f"inline_button_4")

            inline_keyboard_choose = InlineKeyboardMarkup(row_width=2).add(inline_button_1, inline_button_2,
                                                                           inline_button_3, inline_button_4)
            return inline_keyboard_choose
