from environs import Env
from google.cloud import dialogflow

import config


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

    print(f"Intent created: {display_name}")


def create_intents(file, project_id):
    training_file = config.get_training_file(file)
    intents = config.get_intents(training_file)

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


if __name__ == "__main__":
    env = Env()
    env.read_env()

    dialog_flow_project_id = env('DIALOG_FLOW_ID_PROJECT')
    get_training_file = 'train_phrase_1.json'

    create_intents(get_training_file, dialog_flow_project_id)