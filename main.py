
from aiogram.utils import executor
import handler.handlers_comand
from bot_init import dp
from handler import *

# handler.ignore.register_handler_commands_command_ignore(dp)

handler.handlers.register_handler_command(dp)
handlers_bu_inline.register_handler_command_bu_inline(dp)
handler.handlers_comand.register_handler_commands_command(dp)

executor.start_polling(dp, skip_updates=True)
