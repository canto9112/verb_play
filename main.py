import logging

import telegram
from environs import Env

import telegram_bot
import vk_bot
from logger_bot import MyLogsHandler

telegram_logger = logging.getLogger('tg-bot')


def main():
    env = Env()
    env.read_env()

    vk_token = env('VK_TOKEN')
    telegram_token = env('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = env('TELEGRAM_CHAT_ID')
    dialog_flow_project_id = env('DIALOG_FLOW_ID_PROJECT')
    language = "ru-RU"

    bot = telegram.Bot(token=telegram_token)

    telegram_logger.setLevel(logging.DEBUG)
    telegram_logger.addHandler(MyLogsHandler(bot, telegram_chat_id))

    telegram_logger.debug('Бот ВК и Telegram - запущен')
    try:
        telegram_bot.start_telegram_bot(telegram_token, dialog_flow_project_id, language, telegram_chat_id)
        vk_bot.start_vk_bot(vk_token, dialog_flow_project_id, language)
    except telegram.error.NetworkError:
        telegram_logger.error('Бот упал с ошибкой - NetworkError')


if __name__ == '__main__':
    main()

