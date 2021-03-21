from dotenv import load_dotenv
import telegram_bot
import vk_bot
import os


def main():
    load_dotenv()

    vk_token = os.getenv('VK_TOKEN')
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')

    language = "ru-RU"
    dialog_flow_project_id = os.getenv('DIALOG_FLOW_ID_PROJECT')

    telegram_bot.start_telegram_bot(telegram_token, dialog_flow_project_id, language)
    vk_bot.start_vk_bot(vk_token, dialog_flow_project_id, language)


if __name__ == '__main__':
    main()

