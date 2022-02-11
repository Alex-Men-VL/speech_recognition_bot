from environs import Env

env = Env()
env.read_env()

tg_token = env.str('TELEGRAM_BOT_TOKEN')
project_id = env.str('PROJECT_ID')
language_code = env.str('LANGUAGE_CODE', 'ru')
tg_dev_chat_id = env.str('TG_DEV_CHAT_ID')
