import logging

from environs import Env

from config import (
    tg_token,
    project_id,
    language_code
)
from tg_bot import TgBot

logger = logging.getLogger('tg_bot')

env = Env()
env.read_env()


def start_bot():
    bot = TgBot(
        tg_token=tg_token,
        project_id=project_id,
        language_code=language_code
    )
    bot.updater.start_polling()
    bot.updater.idle()


def main():
    try:
        start_bot()
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    main()
