import dotenv
from pyowm.utils.config import get_default_config
import os

dotenv.load_dotenv()


def get_parent_dirname() -> str:
        """Возвращает название родительской директории проекта"""

        return os.path.relpath(os.getcwd(), os.path.dirname(os.getcwd()))


class Config:
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
    quote_url = os.getenv('QUOTE_URL')

    at_usrname = os.getenv('ATERNOS_USERNAME')
    at_pass = os.getenv('ATERNOS_PASSWORD')
    
