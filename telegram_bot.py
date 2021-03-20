import logging

from environs import Env
from telegram.ext import Filters, MessageHandler, Updater

import config


def handle_text(bot, update):
    language = "ru-RU"
    project_id = env('DIALOG_FLOU_ID_PROJECT')

    user_id = update.message.chat_id
    username = update.message.chat['username']
    user_message = update.message.text

    fulfillment_text, fallback_intent = config.detect_intent_texts(project_id, user_id, user_message, language)
    bot.sendMessage(chat_id=user_id, text=fulfillment_text)
    logger.info(f'User id/name: {user_id}/{username}, message: {user_message}, bot response: {fulfillment_text}')


def start_polling(token):
    updater = Updater(token=token)
    # MessageHandler -- более универсальный обработчик, который берёт на вход фильтр
    text_handler = MessageHandler(Filters.text, handle_text)
    # регистрируем свеженькие обработчики в диспетчере
    updater.dispatcher.add_handler(text_handler)
    updater.start_polling()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    logger = config.get_logger()

    token = env('TELEGRAM_BOT_TOKEN')

    start_polling(token)
