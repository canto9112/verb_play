from environs import Env
from telegram.ext import Filters, MessageHandler, Updater

import config

env = Env()
env.read_env()


def handle_text(bot, update):
    logger = config.get_logger()

    language = "ru-RU"
    project_id = env('DIALOG_FLOW_ID_PROJECT')

    user_id = update.message.chat_id
    username = update.message.chat['username']
    user_message = update.message.text

    fulfillment_text, fallback_intent = config.detect_intent_texts(project_id, user_id, user_message, language)
    bot.sendMessage(chat_id=user_id, text=fulfillment_text)
    logger.info(f'User id/name: {user_id}/{username}, message: {user_message}, bot response: {fulfillment_text}')


def starting_telegram_bot():
    token = env('TELEGRAM_BOT_TOKEN')

    updater = Updater(token=token)
    # MessageHandler -- более универсальный обработчик, который берёт на вход фильтр
    text_handler = MessageHandler(Filters.text, handle_text)
    # регистрируем свеженькие обработчики в диспетчере
    updater.dispatcher.add_handler(text_handler)
    updater.start_polling()
