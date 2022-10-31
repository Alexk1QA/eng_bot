from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionParams(StatesGroup):
    """Машина состояний для Б/У"""

    start_bu = State()

    add_word_first = State()
    add_word_last = State()
    add_word_replay = State()
    add_word_quit = State()

    question_model = State()
    question_year = State()
    question_price = State()
    question_fuel = State()
    question_kpp = State()
    question_volume = State()

    question_ended = State()


