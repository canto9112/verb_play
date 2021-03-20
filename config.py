import json
import logging


def get_logger():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


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
