from environs import Env
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import config


def send_message(event, vk_api, user_id):
    vk_api.messages.send(
        user_id=user_id,
        message=event,
        random_id=random.randint(1, 1000)
    )


def starting_vk_bot():
    env = Env()
    env.read_env()
    token = env('VK_TOKEN')

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    language = "ru-RU"
    project_id = env('DIALOG_FLOW_ID_PROJECT')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id
            user_message = event.text

            fulfillment_text, fallback_intent = config.detect_intent_texts(project_id, user_id, user_message, language)
            if not fallback_intent:
                send_message(fulfillment_text, vk_api, user_id)
