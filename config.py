import json
import logging

from google.cloud import dialogflow


def get_logger():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def get_contents_file(file):
    with open(file, "r") as my_file:
        file_contents = json.load(my_file)
    return file_contents


def get_intents(contents):
    intents = []

    for name_intent, result in contents.items():
        messages = result['answer']
        questions = result['questions']

        training_phrases = []
        for question in questions:
            training_phrases.append({'parts': question})
        intents.append({'display_name': name_intent,
                        "messages": {"text": [messages]},
                        'training_phrases': training_phrases
                        })
    return intents


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print(f"Session path: {session}\n")
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    params = {"session": session,
              "query_input": query_input}
    response = session_client.detect_intent(request=params)

    response_result = response.query_result
    fulfillment_text = response_result.fulfillment_text
    fallback_intent = response_result.intent.is_fallback
    return fulfillment_text, fallback_intent


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:

        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part['parts'])
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])

        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts['text'])
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    params = {"parent": parent,
              "intent": intent}
    response = intents_client.create_intent(request=params)

    print(f"Intent created: {display_name}")
