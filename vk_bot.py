from environs import Env
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import detect_intent_google

def vk_bot(token):
    vk_session = vk_api.VkApi(token=token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение от:', event.user_id)
            if event.to_me:
                print('Для меня от: ', event.user_id)
                print('Текст:', event.text)
            else:
                print('От меня для: ', event.user_id)
                print('Текст:', event.text)


def echo(event, vk_api, user_id):
    vk_api.messages.send(
        user_id=user_id,
        message=event,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    token = env('VK_TOKEN')

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    language = "ru-RU"
    project_id = env('DIALOG_FLOU_ID_PROJECT')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id
            user_message = event.text

            fulfillment_text, fallback_intent = detect_intent_google.detect_intent_texts(project_id, user_id, user_message, language)
            if not fallback_intent:
                echo(fulfillment_text, vk_api, user_id)

