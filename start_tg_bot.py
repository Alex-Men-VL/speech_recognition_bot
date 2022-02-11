import logging

from config import (
    tg_token,
    tg_dev_chat_id,
    project_id,
    language_code,
)
from tg_bot import TgBot, TelegramLogsHandler

logger = logging.getLogger('tg_bot')


def start_tg_bot():
    bot = TgBot(
        tg_token=tg_token,
        project_id=project_id,
        language_code=language_code
    )
    logs_handler = TelegramLogsHandler(bot.updater.bot, tg_dev_chat_id)
    logger.addHandler(logs_handler)
    logger.info('Telegram bot is running')

    bot.updater.start_polling()
    bot.updater.idle()


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        start_tg_bot()
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    main()