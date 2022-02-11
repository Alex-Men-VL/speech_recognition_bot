import logging

from config import vk_token
from vk_bot import VkBot


logger = logging.getLogger(__file__)


def main():
    logging.basicConfig(level=logging.INFO)

    bot = VkBot(
        vk_token=vk_token
    )
    for event in bot.longpoll.listen():
        bot.handle_message(event)


if __name__ == '__main__':
    main()
