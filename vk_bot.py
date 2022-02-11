from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType


class VkBot:

    def __init__(self, vk_token):
        self._vk_session = VkApi(token=vk_token)
        self.longpoll = VkLongPoll(self._vk_session)
        self.bot = self._vk_session.get_api()

    def handle_message(self, event):
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)
