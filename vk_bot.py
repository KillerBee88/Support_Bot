import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from google.cloud import storage
from telegram import Bot
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_helpers import detect_vk_intent_texts

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
client = storage.Client.from_service_account_json(credentials_path)
project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("DEVELOPER_CHAT_ID")


def process_event(event, vk_api, logger):
    session_id = event.user_id
    text = event.text
    language_code = 'ru'

    response = detect_vk_intent_texts(project_id, session_id, text, language_code)

    if not response.query_result.intent.is_fallback:
        fulfillment_text = response.query_result.fulfillment_text
        vk_api.messages.send(
            user_id=event.user_id,
            message=fulfillment_text,
            random_id=random.randint(1, 1000)
        )
        logger.info(
            f"Sent message to user {event.user_id}: {fulfillment_text}")


def send_telegram_message(text):
    bot = Bot(token=telegram_bot_token)
    bot.send_message(chat_id=telegram_chat_id, text=text)


def main():
    load_dotenv()
    vk_token = os.getenv("VK_BOT_TOKEN")

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                process_event(event, vk_api, logger)
    except Exception as e:
        error_message = f"Возникла ошибка: {str(e)}"
        logger.error(error_message)
        send_telegram_message(
            error_message, telegram_bot_token, telegram_chat_id)


if __name__ == "__main__":
    main()
