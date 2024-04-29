import logging
import os
import random

import vk_api as vk
from google.cloud import dialogflow, storage
from vk_api.longpoll import VkEventType, VkLongPoll
from dotenv import load_dotenv

load_dotenv()

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
client = storage.Client.from_service_account_json(credentials_path)
vk_token = os.getenv("VK_BOT_TOKEN")
project_id = os.getenv("DIALOGFLOW_PROJECT_ID")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    return response


def echo(event, vk_api):
    session_id = event.user_id
    text = event.text
    language_code = 'ru'

    if text.lower() == 'error':
        raise Exception("Тестовая ошибка")

    response = detect_intent_texts(project_id, session_id, text, language_code)

    if not response.query_result.intent.is_fallback:
        fulfillment_text = response.query_result.fulfillment_text
        vk_api.messages.send(
            user_id=event.user_id,
            message=fulfillment_text,
            random_id=random.randint(1, 1000)
        )
        logger.info(f"Sent message to user {event.user_id}: {fulfillment_text}")

if __name__ == "__main__":
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
