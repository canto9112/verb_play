import argparse
import json

from environs import Env
from google.cloud import dialogflow


def get_training_file(file):
    with open(file, "r") as my_file:
        file_contents = json.load(my_file)
    return file_contents


def get_intents(contents):
    intents = []

    for name_intent, result in contents.items():
        messages = result['answer']
        questions = result['questions']

        training_phrases_parts = []
        for question in questions:
            training_phrases_parts.append({'parts': question})
        intents.append({'display_name': name_intent,
                        "messages": {"text": [messages]},
                        'training_phrases_parts': training_phrases_parts
                        })
    return intents


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part['parts'])
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts['text'])
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    params = {"parent": parent,
              "intent": intent}
    intents_client.create_intent(request=params)


def create_intents(file, project_id):
    training_file = get_training_file(file)
    intents = get_intents(training_file)

    for intent in intents:
        display_name = intent['display_name']
        training_phrases_parts = intent['training_phrases_parts']
        messages = intent['messages']
        create_intent(project_id, display_name, training_phrases_parts, messages)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    params = {"session": session,
              "query_input": query_input}
    response = session_client.detect_intent(request=params)

    response_result = response.query_result
    fulfillment_text = response_result.fulfillment_text
    fallback_intent = response_result.intent.is_fallback

    return fulfillment_text, fallback_intent


def get_args():
    parser = argparse.ArgumentParser(
        description='Скрипт принимает файл с заготовленными вопросами и ответами'
    )
    parser.add_argument('file', help='Название json файла для обучения бота')
    args = parser.parse_args()
    return args.file


def main():
    env = Env()
    env.read_env()

    dialog_flow_project_id = env('DIALOG_FLOW_ID_PROJECT')

    training_file = get_args()

    create_intents(training_file, dialog_flow_project_id)


if __name__ == "__main__":
    main()
