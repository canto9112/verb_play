from environs import Env

import telegram_bot
import vk_bot


def main():
    env = Env()
    env.read_env()

    vk_token = env('VK_TOKEN')
    telegram_token = env('TELEGRAM_BOT_TOKEN')

    language = "ru-RU"
    dialog_flow_project_id = env('DIALOG_FLOW_ID_PROJECT')

    telegram_bot.start_telegram_bot(telegram_token, dialog_flow_project_id, language)
    vk_bot.start_vk_bot(vk_token, dialog_flow_project_id, language)


if __name__ == '__main__':
    main()

