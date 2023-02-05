import dotenv
from pyowm.utils.config import get_default_config
import os
import json

dotenv.load_dotenv()



def get_parent_dirname() -> str:
        """Возвращает название родительской директории проекта"""

        return os.path.relpath(os.getcwd(), os.path.dirname(os.getcwd()))


class Config:
    
    def _get_json(path : str) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
        return content
    
    __commands_file_path = os.getenv('COMMANDS_FILE_PATH')
    __news_categories_file_path = os.getenv('NEWS_CATEGORIES_FILE_PATH')
    __phrases_file_path = os.getenv('PHRASES_FILE_PATH')

    yand_api_key = os.getenv('YANDEX_API_KEY')
    bot_token = os.getenv('BOT_TOKEN')
    pyowm_api_key = os.getenv('PYOWM_API_KEY')

    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    config_dict['connection']['use_ssl'] = False
    config_dict['connection']["verify_ssl_certs"] = False

    parent_dirname = get_parent_dirname()

    guild_id = os.getenv('GUILD_ID')
    suntime_url = os.getenv('SUNTIME_URL')
    host = os.getenv('HOST')
    news_url = os.getenv('NEWS_URL')
    news_api_key = os.getenv('NEWS_API_KEY')
    quote_url = os.getenv('QUOTE_URL')

    at_usrname = os.getenv('ATERNOS_USERNAME')
    at_pass_hashed = os.getenv('ATERNOS_PASSWORD_HASH')
    
    database_path = os.getenv('DATABASE_PATH')


    common_help = _get_json(__commands_file_path)['common_help']
    aternos_help = _get_json(__commands_file_path)['aternos_help']
    news_categories = _get_json(__news_categories_file_path)
    welcomes = _get_json(__phrases_file_path)['welcomes']
    greetings = _get_json(__phrases_file_path)['greetings']



