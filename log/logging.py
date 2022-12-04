import logging


def logger_(user_id, error_):

    logger = logging.getLogger(__name__)

    # f_handler = logging.FileHandler(f"/Users/macbook/Desktop/english_bot_test/logs_users/log_{user_id}.log")
    f_handler = logging.FileHandler(f"/home/ubuntu/eng_bot/logs_users/log_{user_id}.log")

    f_handler.setLevel(logging.WARNING)
    f_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.warning(error_)
