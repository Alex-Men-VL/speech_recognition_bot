import argparse
import json
import logging

from google.api_core.exceptions import BadRequest
from google.cloud import dialogflow

from config import project_id

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Add new intent')
    parser.add_argument('--path', '-p',
                        help='Enter the path to the json file',
                        default='questions.json')
    return parser.parse_args()


def create_intent(display_name, intent_options):
    training_phrases_parts = intent_options['questions']
    message_texts = [intent_options['answer']]

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    intents_client.create_intent(
        request={
            'parent': parent,
            'intent': intent
        }
    )


def main():
    logging.basicConfig(level=logging.INFO)

    args = parse_arguments()
    json_path = args.path

    with open(json_path, 'r') as json_file:
        intents = json.load(json_file)

    for display_name, intent_options in intents.items():
        try:
            create_intent(display_name, intent_options)
        except BadRequest as err:
            logger.error(
                f"Intent with the name '{display_name}' not loaded.\n{err}\n"
            )
        else:
            logger.info(
                f"Intent with the name '{display_name}' loaded.\n"
            )


if __name__ == '__main__':
    main()
