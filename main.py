from aiogram.utils import executor
from bot_init import dp
import handler


def main():

    handler.handlers.register_handler_command(dp)
    handler.handlers_comand.register_handler_commands_command(dp)
    handler.handlers_add_data.register_handler_command_add_data(dp)
    handler.handlers_test_mode.register_handler_command_test_mode(dp)
    handler.handlers_settings.register_handler_command_settings(dp)
    handler.handlers_replay_inline.register_handler_command_bu_inline(dp)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
