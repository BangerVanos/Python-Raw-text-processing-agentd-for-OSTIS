"""That file contains configurations for raw text processing
agents."""

# Prompts
PROMPTS = {'lang_en': 'I have sentences divided by semicolons. Connect those sentences in one human-readable text.'
                      'Connect some sentences in one if possible. Drop repeatable information.'
                      'Do not add information which is not represented in sentences. Give only answer. {!s}',
           'lang_ru': 'У меня есть предложения, разделённые точкой с запятой. Соедини эти предложения в читаемый текст.'
                      'Объедини некоторые предложения в одно, если возможно. Убери повторяющуюся информацию.'
                      'Не добавляй информацию, которой нет в предложениях. Дай только ответ. {!s}'
           }

# Configs for non official API agent
NON_OFFICIAL_API_DEFAULT_MODEL = 'gpt-3.5-turbo'
NON_OFFICIAL_API_AGENT_ACTION = 'action_get_clean_text_using_non_official_api'

# Configs for local language model agent
LOCAL_MODEL_PATH = 'PUT_YOR_LLAMA2_PATH_HERE'
LOCAL_MODEL_AGENT_ACTION = 'action_get_clean_text_using_local_model'

# Configs for official API agent
OPENAI_TOKEN = 'PUT_YOUR_OPEN_AI_TOKEN_HERE'
BARD_TOKEN = 'PUT_YOUR_BARD_TOKEN_HERE'
OFFICIAL_API_AGENT_ACTION = 'action_get_clean_text_using_official_api'
