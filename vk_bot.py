import random

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType


class VkBot:

    def __init__(self, vk_token):
        self._vk_session = VkApi(token=vk_token)
        self.longpoll = VkLongPoll(self._vk_session)
        self.bot = self._vk_session.get_api()

    def handle_message(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            self.bot.messages.send(
                user_id=event.user_id,
                message=event.text,
                random_id=random.randint(1, 1000)
            )
