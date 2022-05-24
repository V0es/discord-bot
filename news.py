from typing import List
import web
from config import Config as cfg

def get_news():
    page = web.get_request(cfg.news_url)
    soup = web.make_soup(page)
    dirt_news = soup.find_all('div', class_='mg-card__text-content')
    filtered_news = []
    # print(dirt_news)
    for data in dirt_news:
        if data.find('h2', class_='mg-card__title') is not None:
            filtered_news.append(data.find('h2', class_='mg-card__title').text)

    for i in range(len(filtered_news)):
        filtered_news[i] = filtered_news[i].replace('\xa0', ' ')
    
    formatted_news = format_news(filtered_news)
    return formatted_news


def format_news(news : List) -> str:
    news_f = ''
    for i in range(15):
        news_f = news_f + news[i] + '\n\n'
    return news_f

