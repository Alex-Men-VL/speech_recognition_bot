import logging
import random
from dataclasses import dataclass

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll

from dialogflow_utils import detect_intent_texts


@dataclass(eq=False)
class Bot:

    token: str
    project_id: str
    language_code: str


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


class TgBot(Bot):

    def __init__(self, token, project_id, language_code):
        super().__init__(token, project_id, language_code)
        self.updater = Updater(token=token, use_context=True)
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self.handle_message)
        )
        self.updater.dispatcher.add_handler(
            CommandHandler('start', self.handle_start_message)
        )

    def handle_message(self, update: Update, _):
        chat_id = update.message.chat_id
        received_message = update.message.text

        message = detect_intent_texts(self.project_id, chat_id, received_message, self.language_code)
        update.message.reply_text(message.fulfillment_text)

    @staticmethod
    def handle_start_message(update: Update, _):
        user = update.effective_user
        update.message.reply_text(f'Привет, {user.first_name}!')


class VkBot(Bot):

    def __init__(self, token, project_id, language_code):
        super().__init__(token, project_id, language_code)
        self._vk_session = VkApi(token=token)
        self.longpoll = VkLongPoll(self._vk_session)
        self.bot = self._vk_session.get_api()

    def handle_message(self, event):
        user_id = event.user_id,
        received_message = event.text
        message = detect_intent_texts(self.project_id, user_id, received_message, self.language_code)

        if not message.intent.is_fallback:
            self.bot.messages.send(
                user_id=user_id,
                message=message.fulfillment_text,
                random_id=random.randint(1, 1000)
            )
