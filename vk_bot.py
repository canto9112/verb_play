import logging
import random

import vk_api as vk
from vk_api.longpoll import VkEventType, VkLongPoll

import create_intents

telegram_logger = logging.getLogger('tg-bot')


def send_message(event, vk_api, user_id):
    vk_api.messages.send(
        user_id=user_id,
        message=event,
        random_id=random.randint(1, 1000)
    )


def start_vk_bot(token, project_id, language):
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id
            user_message = event.text

            fulfillment_text, fallback_intent = create_intents.detect_intent_texts(project_id, f'vk-{user_id}', user_message, language)
            if not fallback_intent:
                send_message(fulfillment_text, vk_api, user_id)
            else:
                telegram_logger.debug(f'В Вконтакте юзеру: {user_id} бот не знает что ответить. \nВот что он спросил: \n{user_message}')
