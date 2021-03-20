import config


def create_intents(file):
    training_phrases = config.get_contents_file(file)
    intents = config.get_intents(training_phrases)
    for intent in intents:
        display_name = intent['display_name']
        training_phrases = intent['training_phrases']
        messages = intent['messages']
        config.create_intent('verb3-307417', display_name, training_phrases, messages)


if __name__ == "__main__":
    train_phrase = 'train_phrase_1.json'
    create_intents(train_phrase)