import argparse
import json
import os

from google.cloud import dialogflow_v2 as dialogflow

project_id = os.getenv('DIALOGFLOW_PROJECT_ID')


def create_intent(project_id, display_name, training_phrases_parts, message_text):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for part_text in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(text=part_text)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=[message_text])
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent})

    return response


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Укажите путь к файлу .json')
    parser.add_argument('data_file_path', type=str,
                        help='Path to the data file')
    args = parser.parse_args()

    with open(args.data_file_path) as file:
        data = json.load(file)

    for intent_name, intent_data in data.items():
        create_intent(
            project_id,
            intent_name,
            intent_data['questions'],
            intent_data['answer']
        )
