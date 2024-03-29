from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionParams(StatesGroup):

    add_word_first = State()
    add_word_last = State()
    add_word_quit = State()

    question_test = State()

    user_settings_update = State()

    update_word = State()
