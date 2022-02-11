import logging

from config import (
    tg_token,
    project_id,
    language_code,
)
from tg_bot import TgBot

logger = logging.getLogger('tg_bot')


def start_tg_bot():
    bot = TgBot(
        tg_token=tg_token,
        project_id=project_id,
        language_code=language_code
    )
    logger.info('The tg bot is running')
    bot.updater.start_polling(drop_pending_updates=True)
    bot.updater.idle()


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        start_tg_bot()
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    main()
