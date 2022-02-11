import logging

from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


class TgBot:

    def __init__(self, tg_token, project_id, language_code):
        self.tg_token = tg_token
        self.project_id = project_id
        self.language_code = language_code
        self.updater = Updater(token=tg_token, use_context=True)
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self.handle_message)
        )
        self.updater.dispatcher.add_handler(
            CommandHandler('start', handle_start_message)
        )

    def handle_message(self, update: Update, _):
        chat_id = update.message.chat_id
        received_message = update.message.text

        message = detect_intent_texts(self.project_id, chat_id, received_message, self.language_code)
        update.message.reply_text(message)


def handle_start_message(update: Update, _):
    user = update.effective_user
    update.message.reply_text(f'Привет, {user.first_name}!')


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={
            "session": session,
            "query_input": query_input
        }
    )
    return response.query_result.fulfillment_text
