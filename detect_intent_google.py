from google.cloud import dialogflow
import json
from pprint import pprint


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print(f"Session path: {session}\n")
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    params = {"session": session,
              "query_input": query_input}
    response = session_client.detect_intent(request=params)
    #
    # print("=" * 20)
    # print("Query text: {}".format(response.query_result.query_text))
    # print(
    #     "Detected intent: {} (confidence: {})\n".format(
    #         response.query_result.intent.display_name,
    #         response.query_result.intent_detection_confidence,
    #     )
    # )
    # print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    return response.query_result.fulfillment_text


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
