import json


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

