import os
import random

import vk_api as vk
from google.cloud import dialogflow
from vk_api.longpoll import VkEventType, VkLongPoll

vk_token = os.getenv("VK_BOT_TOKEN")
project_id = os.getenv("DIALOGFLOW_PROJECT_ID")


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    return response


def echo(event, vk_api):
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
    session_id = event.user_id
    text = event.text
    language_code = 'ru'

    response = detect_intent_texts(project_id, session_id, text, language_code)

    if not response.query_result.intent.is_fallback:
        fulfillment_text = response.query_result.fulfillment_text
        vk_api.messages.send(
            user_id=event.user_id,
            message=fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
