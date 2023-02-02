import requests
from bs4 import BeautifulSoup
from config.config import Config as cfg

def get_request(url, params=None, headers=None):
    """Функция отравляет GET-запрос по указанному URL-адресу с указанными параметрами и заголовками
        Возвращает объет типа Response"""
    answer = requests.get(url, params=params, headers=headers)
    return answer


def make_soup(page):
    """Возвращает объект soup для дальнейшей работы"""
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def get_random_guote():
    """Возвращает текст цитаты"""
    html = get_request(cfg.quote_url)
    soup = make_soup(html)
    return soup.text
