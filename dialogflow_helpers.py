import os

from google.cloud import dialogflow

dialogflow_client = dialogflow.SessionsClient()


def detect_intent_texts(project_id, session_id, text, language_code, client):
    session = client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response
