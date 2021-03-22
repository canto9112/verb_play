import logging

from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

import create_intents

telegram_logger = logging.getLogger('tg-bot')


def handle_text(update, context: CallbackContext):
    language = context.bot_data['language']
    project_id = context.bot_data['project_id']

    user_id = update.message.chat_id
    username = update.message.chat['username']
    user_message = update.message.text

    fulfillment_text, fallback_intent = create_intents.detect_intent_texts(project_id, user_id, user_message, language)

    context.bot.sendMessage(chat_id=user_id, text=fulfillment_text)
    if fallback_intent:
        telegram_logger.debug(f'В Телеграме юзеру {username} бот не знает что ответить. \nВот что {username} спросил: \n{user_message}')


def start_telegram_bot(token, project_id, language, tg_chat_id):
    updater = Updater(token=token)
    # MessageHandler -- более универсальный обработчик, который берёт на вход фильтр
    text_handler = MessageHandler(Filters.text, handle_text)
    # регистрируем свеженькие обработчики в диспетчере
    updater.dispatcher.add_handler(text_handler)
    updater.dispatcher.bot_data['project_id'] = project_id
    updater.dispatcher.bot_data['language'] = language
    updater.dispatcher.bot_data['tg_chat_id'] = tg_chat_id

    updater.start_polling()
