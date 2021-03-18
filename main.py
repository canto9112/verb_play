from environs import Env
from telegram.ext import MessageHandler, Filters, Updater
import detect_intent_google
import logging
import train_phrases_json
from pprint import pprint


def handle_text(bot, update):
    language = "ru-RU"
    project_id = env('DIALOG_FLOU_ID_PROJECT')

    user_id = update.message.chat_id
    username = update.message.chat['username']
    user_message = update.message.text

    bot_response = detect_intent_google.detect_intent_texts(project_id, user_id, user_message, language)
    bot.sendMessage(chat_id=user_id, text=bot_response)
    logger.info(f'User id/name: {user_id}/{username}, message: {user_message}, bot response: {bot_response}')


def start_polling(token):
    updater = Updater(token=token)
    # MessageHandler -- более универсальный обработчик, который берёт на вход фильтр
    text_handler = MessageHandler(Filters.text, handle_text)
    # регистрируем свеженькие обработчики в диспетчере
    updater.dispatcher.add_handler(text_handler)
    updater.start_polling()


def create_intents(file):
    training_phrases = train_phrases_json.get_contents_file(file)
    intents = train_phrases_json.get_intents(training_phrases)
    for intent in intents:
        display_name = intent['display_name']
        training_phrases = intent['training_phrases']
        messages = intent['messages']
        detect_intent_google.create_intent('verb3-307417', display_name, training_phrases, messages)


def get_logger():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


if __name__ == '__main__':
    env = Env()
    env.read_env()
    logger = get_logger()

    token = env('TELEGRAM_BOT_TOKEN')
    train_phrase = 'train_phrase_1.json'

    start_polling(token)
    # create_intents(train_phrase)
    # intents_list = detect_intent_google.list_intents('verb3-307417')

