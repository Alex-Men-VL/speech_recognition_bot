import logging
import random

from environs import Env
from telegram import Bot
from vk_api import VkApi
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_utils import detect_intent_texts
from tg_logs_handler import TelegramLogsHandler

logger = logging.getLogger(__file__)

env = Env()
env.read_env()


def handle_message(event, bot, project_id, language_code):
    user_id = event.user_id,
    received_message = event.text
    message = detect_intent_texts(project_id, user_id, received_message, language_code)

    if not message.intent.is_fallback:
        bot.messages.send(
            user_id=user_id,
            message=message.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    logging.basicConfig(level=logging.INFO)

    project_id = env.str('PROJECT_ID')
    language_code = env.str('LANGUAGE_CODE', 'ru')
    tg_dev_token = env.str('TELEGRAM_DEV_BOT_TOKEN')
    tg_dev_chat_id = env.str('TG_DEV_CHAT_ID')
    vk_token = env.str('VK_BOT_TOKEN')

    dev_bot = Bot(token=tg_dev_token)
    logs_handler = TelegramLogsHandler(dev_bot, tg_dev_chat_id)
    logger.addHandler(logs_handler)
    logger.info('VK bot is running')

    try:
        vk_session = VkApi(token=vk_token)
        longpoll = VkLongPoll(vk_session)
        bot = vk_session.get_api()

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                handle_message(event, bot, project_id, language_code)
    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    main()
