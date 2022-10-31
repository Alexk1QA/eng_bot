from aiogram import Dispatcher
from keyboard.keyboard_bu_inline import *
from bot_init import bot
from aiogram.types import CallbackQuery


async def manual(call: CallbackQuery):
    numb_buttom = call.data[-1]

    actual_dict_param = update_keyboard_main(numb_buttom)

    await bot.answer_callback_query(call.id, text='Изменения внесены')

    await call.message.edit_reply_markup(keyboard_choose())


def register_handler_command_bu_inline(dp: Dispatcher):
    dp.register_callback_query_handler(manual, lambda c: c.data.startswith('inline'))
