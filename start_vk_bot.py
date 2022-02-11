import logging

from vk_api.longpoll import VkEventType

from bots import VkBot
from config import (
    vk_token,
    project_id,
    language_code
)

logger = logging.getLogger(__file__)


def main():
    logging.basicConfig(level=logging.INFO)

    bot = VkBot(
        token=vk_token,
        project_id=project_id,
        language_code=language_code
    )
    logger.info('VK bot is running')

    for event in bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            bot.handle_message(event)


if __name__ == '__main__':
    main()
