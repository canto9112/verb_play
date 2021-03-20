import logging

from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

import create_intents


def get_logger():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def handle_text(update, context: CallbackContext):
    logger = get_logger()

    language = context.bot_data['language']
    project_id = context.bot_data['project_id']

    user_id = update.message.chat_id
    username = update.message.chat['username']
    user_message = update.message.text

    fulfillment_text, fallback_intent = create_intents.detect_intent_texts(project_id, user_id, user_message, language)
    context.bot.sendMessage(chat_id=user_id, text=fulfillment_text)

    logger.info(f'User id/name: {user_id}/{username}, message: {user_message}, bot response: {fulfillment_text}')


def start_telegram_bot(token, project_id, language):
    updater = Updater(token=token)
    # MessageHandler -- более универсальный обработчик, который берёт на вход фильтр
    text_handler = MessageHandler(Filters.text, handle_text)
    # регистрируем свеженькие обработчики в диспетчере
    updater.dispatcher.add_handler(text_handler)
    updater.dispatcher.bot_data['project_id'] = project_id
    updater.dispatcher.bot_data['language'] = language

    updater.start_polling()
