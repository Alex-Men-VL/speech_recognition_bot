import argparse
import json
import logging
import os

from environs import Env
from google.api_core.exceptions import BadRequest

from dialogflow_utils import create_intent

logger = logging.getLogger(__file__)

env = Env()
env.read_env()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Add new intent')
    parser.add_argument('--path', '-p',
                        help='Enter the path to the json file',
                        default=os.path.join('files', 'questions.json'))
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO)

    project_id = env.str('PROJECT_ID')

    args = parse_arguments()
    json_path = args.path

    with open(json_path, 'r') as json_file:
        intents = json.load(json_file)

    for display_name, intent_options in intents.items():
        try:
            create_intent(project_id, display_name, intent_options)
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
