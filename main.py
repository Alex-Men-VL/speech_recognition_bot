import logging
from environs import Env

from tg_bot import TgBot

logger = logging.getLogger('tg_bot')

env = Env()
env.read_env()


def start_bot():
    tg_token = env.str('TELEGRAM_BOT_TOKEN')
    bot = TgBot(
        tg_token=tg_token
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