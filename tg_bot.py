from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)


class TgBot:

    def __init__(self, tg_token):
        self.tg_token = tg_token
        self.updater = Updater(token=tg_token, use_context=True)
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, handle_message)
        )
        self.updater.dispatcher.add_handler(
            CommandHandler('start', handle_start_message)
        )


def handle_start_message(update: Update, _):
    user = update.effective_user
    update.message.reply_text(f'Привет, {user.first_name}.')


def handle_message(update: Update, _):
    user_message = update.message.text
    update.message.reply_text(user_message)
