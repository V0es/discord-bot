from typing import List
import web
from config import Config as cfg

def get_news():
    """Функция возвращает спискок заголовков новостей"""
    page = web.get_request(cfg.news_url)
    soup = web.make_soup(page)
    dirt_news = soup.find_all('div', class_='mg-card__text-content') # поиск по конкретному div'у
    filtered_news = []
    for data in dirt_news:
        if data.find('h2', class_='mg-card__title') is not None:
            filtered_news.append(data.find('h2', class_='mg-card__title').text) # если есть текст заголовка - помещаем в список

    for i in range(len(filtered_news)):
        filtered_news[i] = filtered_news[i].replace('\xa0', ' ') # заменяем служебные символы на обычные
    
    formatted_news = format_news(filtered_news)
    return formatted_news


def format_news(news : List) -> str:
    """Функция принимает на вход список заголовков новостей
    Компонует в строку первые 15 заголовков, и возвращает"""
    news_f = ''
    for i in range(8):
        #news_f = news_f + news[i] + '\n\n'
        print(news)
    return news_f

