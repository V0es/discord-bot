from typing import List, Dict
from random import shuffle

import utils.web as web
from config.config import Config as cfg
from discord import Embed


def get_news(category: str, keyword: str, amount: int) -> List[Embed]:
    """Функция возвращает JSON с новостями"""

    params = {
        'apiKey': cfg.news_api_key,
        'q': keyword,
        'category': category,
        'country': 'ru',
    }

    if not keyword:
        del params['q']
    if not category:
        del params['category']
    if not amount:
        # params['pageSize'] = 7 #default
        amount = 5
        # TODO: проверить правильность передачи параметра количества новостей
    response = web.get_request(cfg.news_url, params=params).json()
    embed_list = _news_embed_list(response, amount)

    return embed_list


def _news_embed_list(response_json: Dict, amount: int) -> List[Embed]:
    """Функция принимает на вход список заголовков новостей
    Компонует в строку первые 15 заголовков, и возвращает"""
    news_list = []
    shuffle(response_json['articles'])
    for item in response_json['articles'][:int(amount)]:
        embed = Embed(title=item['title'], description=item['description'])
        embed.add_field(name='Автор', value=item['author'] if bool(item['author']) else item['source']['name'])
        embed.add_field(name='Ссылка', value=item['url'])
        embed.set_author(name=item['source']['name'], url='https://www.' + item['source']['name'].lower())
        embed.set_image(url=item['urlToImage'])
        news_list.append(embed)
    return news_list
