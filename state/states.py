from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionParams(StatesGroup):
    """Машина состояний для Б/У"""

    add_word_first = State()
    add_word_last = State()
    add_word_replay = State()
    add_word_quit = State()




