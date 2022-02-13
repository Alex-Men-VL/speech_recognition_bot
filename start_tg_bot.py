import logging

from environs import Env
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

from dialogflow_utils import detect_intent_texts
from tg_logs_handler import TelegramLogsHandler

logger = logging.getLogger(__file__)

env = Env()
env.read_env()


def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    received_message = update.message.text

    message = detect_intent_texts(
        context.bot_data.get('project_id'),
        chat_id,
        received_message,
        context.bot_data.get('language_code')
    )
    update.message.reply_text(message.fulfillment_text)


def handle_start_message(update: Update, _):
    user = update.effective_user
    update.message.reply_text(f'Привет, {user.first_name}!')


def main():
    logging.basicConfig(level=logging.INFO)

    tg_token = env.str('TELEGRAM_BOT_TOKEN')
    project_id = env.str('PROJECT_ID')
    language_code = env.str('LANGUAGE_CODE', 'ru')
    tg_dev_token = env.str('TELEGRAM_DEV_BOT_TOKEN')
    tg_dev_chat_id = env.str('TG_DEV_CHAT_ID')

    dev_bot = Bot(token=tg_dev_token)
    logs_handler = TelegramLogsHandler(dev_bot, tg_dev_chat_id)
    logger.addHandler(logs_handler)
    logger.info('Telegram bot is running')

    updater = Updater(token=tg_token, use_context=True)
    updater.dispatcher.bot_data.update(
        {
            'project_id': project_id,
            'language_code': language_code,
        }
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
    )
    updater.dispatcher.add_handler(
        CommandHandler('start', handle_start_message)
    )

    try:
        updater.start_polling()
        updater.idle()
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    main()
