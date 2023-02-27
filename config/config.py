import dotenv
from pyowm.utils.config import get_default_config
import os
import json

dotenv.load_dotenv()


def get_parent_dirname() -> str:
    """Возвращает название родительской директории проекта"""

    return os.path.relpath(os.getcwd(), os.path.dirname(os.getcwd()))


class Config:
    
    def _get_json(path: str) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
        return content
    
    config_json = _get_json('config/config.json')
    deploy_json = _get_json('config/deploy.json')

    yand_api_key = os.getenv('YANDEX_API_KEY')
    discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')
    pyowm_api_key = os.getenv('PYOWM_API_KEY')
    guild_id = os.getenv('GUILD_ID')
    news_api_key = os.getenv('NEWS_API_KEY')

    dockerhub_username = os.getenv('DOCKERHUB_USERNAME')
    dockerhub_password = os.getenv('DOCKERHUB_PASSWORD')
    portainer_username = os.getenv('PORTAINER_USERNAME')
    portainer_password = os.getenv('PORTAINER_PASSWORD')
    dns_username = os.getenv('DNS_USERNAME')
    dns_password = os.getenv('DNS_PASSWORD')
    rpi_address = os.getenv('RPI_ADDRESS')
    endpoint_id = os.getenv('ENDPOINT_ID')

    _deploy = True if os.getenv('DEPLOY') == 'true' else False
    if not _deploy:
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        config_dict['connection']['use_ssl'] = False
        config_dict['connection']["verify_ssl_certs"] = False

    parent_dirname = get_parent_dirname()

    suntime_url = config_json['links']['suntime_url']
    host = config_json['links']['host']
    news_url = config_json['links']['news_url']
    quote_url = config_json['links']['quote_url']
    
    database_path = config_json['paths']['database_path']

    common_help = config_json['available_commands']['common_help']
    aternos_help = config_json['available_commands']['aternos_help']
    news_categories = config_json['news_categories']
    welcomes = config_json['phrases']['welcomes']
    greetings = config_json['phrases']['greetings']
