import discord
import random
import pyowm
from pyowm.utils.config import get_default_config
import time
import os
import requests
from bs4 import BeautifulSoup


yandex_api_key = '593de6af-0e94-4ec9-a34a-c58933c2c20d'
token = 'Njk2NTQ0NTgyNzQxMTMxMjc0.XoqRsQ.aQhnfiSh23GbptjYfGJnaXipJiI'
pyowm_api_key = 'b79bb697bf0d4dacdaa4e6969c13040d'

client = discord.Client()
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM(pyowm_api_key, config=config_dict)
mgr = owm.weather_manager()


status_dict = {
    'clouds': 'облачно',
    'rain': 'дождь',
    'clear': 'ясно',
    'haze': 'туман',
    'snow': 'снег',
    'mist': 'мгла'}

greetings = ['Салам, ', 'Здарова, ', 'Чо каво, сучара. Это мой кореш ', 'Давно не виделись, ', 'Здравствуй, ',
             'И тебе не хворать, ', 'Мы же с тобой уже сегодня виделись, ', 'Привет, ',
             'Ебать, божнур,  ', 'Как же ты меня уже заебал, ', 'Всем хай! И тебе, ']
welcome = ['Вот это да! Кто пожаловал! Это ', 'Добро пожаловать на сервер, ', 'Ой! Кто-то новенький! К нам зашёл ']


localTimeFormat = "%H:%M:%S %d-%m-%Y"


SUNTIME_URL = 'https://api.weather.yandex.ru/v2/forecast/'
HOST = 'https://www.google.com/search'
NEWS_URL = 'https://yandex.ru/news'
QUOTE_URL = 'https://finewords.ru/sluchajnaya?_=1640297828989'


def make_soup(page):
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def get_request(url, params=None, headers=None):
    """Функция отравляет GET-запрос по указанному URL-адресу с указанными параметрами и заголовками
        Возвращает объет типа Response"""
    answer = requests.get(url, params=params, headers=headers)
    return answer


def get_suntime_info(paramspack, headerspack):
    """Данная функция формирует и отправляет GET запрос на сервер на основе полученных параметров,
                    ответ преобразует к удобному для работы виду и возвращает его"""

    answer = get_request(SUNTIME_URL, paramspack, headerspack).json()  # формирую get запрос, ответ перевожу в json
    try:
        answer = list(answer['forecasts'][0].items())
        # беру dict_list всех пар словаря answer и преобразую в list для дальнейшей работы
    except KeyError:
        print('Error accured! Check logs.')
        return
    suntimes = dict([answer[0], answer[3], answer[4], answer[5],
                     answer[6]])  # 'выдёргиваю' из списка нужные пары и складываю новый словарь
    suntimes['date'] = swap_year_day(suntimes['date'])
    return suntimes


def swap_year_day(date):
    """Данная функция приводит дату к более читабельному виду
                (из формата YYYY-MM-DD преобразует в формат DD-MM-YYYY)
        Операция производится в 3 этапа:
        1)Строка разбивается на список из 3 элементов с разделителем '-'.
        2)Меняются местами 2 крайних элемента(день и год).
        3)Список собирается обратно в строку."""

    date = date.split('-')
    tmp = date[0]
    date[0] = date[2]
    date[2] = tmp
    date = '-'.join(date)
    return date


def get_pics_urls(keyword):
    """Функция парсит страницу и вытягивает оттуда адреса исходников картинок в переменную pics"""
    params_dict = {'q': keyword,
                   'tbm': 'isch'}
    pics = []
    page = get_request(HOST, params=params_dict)
    soup = make_soup(page)
    raw_pics = soup.find_all(class_='yWs4tf')
    for data in raw_pics:
        if data.get('src') is not None:
            pics.append(data.get('src'))
    return pics


def get_pic_path(keyword):
    """Функция выбирает рандомную картинку из списка, генерирует имя файла
                                                            и скачивает картинку в этот файл"""
    urls = get_pics_urls(keyword)
    pic_url = urls[random.randint(1, len(urls) - 1)]
    image = get_request(pic_url).content
    img_id = str(time.time_ns())[-6::]
    pic_path = 'images/img'+img_id+'.jpg'
    with open(pic_path, 'wb') as f:
        f.write(image)
    return pic_path


async def delete_pic(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print('Cannot find this file!')


def get_news():
    page = get_request(NEWS_URL)
    soup = make_soup(page)
    dirt_news = soup.find_all('div', class_='mg-card__text-content')
    filtered_news = []
    # print(dirt_news)
    for data in dirt_news:
        if data.find('h2', class_='mg-card__title') is not None:
            filtered_news.append(data.find('h2', class_='mg-card__title').text)

    for i in range(len(filtered_news)):
        filtered_news[i] = filtered_news[i].replace('\xa0', ' ')
    return filtered_news


def get_random_guote():
    html = get_request(QUOTE_URL)
    soup = make_soup(html)
    return soup.text



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    dis_id = client.get_guild(394165433797836801)

    if message.content.find('!hello') != -1:
        num = random.randint(0, len(greetings) - 1)
        await message.channel.send(f'''{greetings[num]}{message.author.name}!''')

    elif message.content == '!help':
        embd = discord.Embed(title='Доступные команды', description='')
        embd.add_field(name='!help', value='Справка по доступным командам')
        embd.add_field(name='!members', value='Количество пользователей на сервере')
        embd.add_field(name='!hello', value='Приветствие пользователя')
        embd.add_field(name='!weather <город>', value='Показывает погоду в указанном городе')
        embd.add_field(name='!suntime <город>', value='Показывает время восхода/захода солнца в указанном городе')
        embd.add_field(name='!pic <запрос>', value='Выдаёт картинку по конкретному запросу')
        embd.add_field(name='!news', value='Выводит актуальные повости')
        embd.add_field(name='!quote', value='Присылает вам случайную цитату')
        await message.channel.send(embed=embd)

    elif message.content.find('!members') != -1:
        members = dis_id.member_count
        await message.channel.send(f'''На сервере {members} участников.''')

    elif message.content.find('!weather') != -1:
        city = message.content[9::]
        print(city)
        try:
            observation = mgr.weather_at_place(city)
        except pyowm.exceptions.api_response_error.NotFoundError:
            await message.channel.send('Я не знаю такого города :(')
            return

        weather = observation.weather
        temperature = weather.temperature('celsius')
        wind = weather.wind('meters_sec')
        hum = weather.humidity
        status = weather.detailed_status
        pressure = weather.pressure
        pressure = round(pressure['press'] * 0.750062, 1)

        await message.channel.send(
            f'''В городе {city} сейчас {str(status)}. 
                Температура: {round(temperature['temp'])}°С. 
                Влажность воздуха: {hum}%. 
                Скорость ветра: {round(wind['speed'])} м/с.
                Атмосферное давление составляет {pressure} мм.рт.ст.''')

    elif message.content.find('!suntime') != -1:
        city = message.content[9::]
        print(city)
        try:
            observation = owm.weather_at_place(city)
        except pyowm.exceptions.api_response_error.NotFoundError:
            await message.channel.send('Я не знаю такого города :(')
            return
        long = observation.get_location().get_lon()
        lat = observation.get_location().get_lat()
        request_dict = {
            'lon': str(long),
            'lat': str(lat),
        }
        headers_dict = {
            'X-Yandex-API-Key': yandex_api_key
        }
        suntimes = get_suntime_info(request_dict, headers_dict)
        try:
            await message.channel.send(f'''    Дата: {suntimes['date']}. 
            Рассвет: начало - {suntimes['rise_begin']}; конец - {suntimes['sunrise']}. 
            Закат: начало - {suntimes['sunset']}; конец - {suntimes['set_end']}''')
        except KeyError:
            await message.channel.send(
                'Упс, похоже вы ввели полярный город, в котором сейчас полярная ночь или полярный день.')

    elif message.content.find('!pic') != -1:
        keyword = message.content[5::]
        print(keyword)
        pic_path = get_pic_path(keyword)
        picture = discord.File(fp=pic_path, filename=keyword+'.jpg')
        await message.channel.send(file=picture)
        await delete_pic(pic_path)

    elif message.content.find('!news') != -1:
        """news_f - отформатированные из спииска в строку новости, 
                                чтобы их можно было вывести одним сообщением"""
        news = get_news()
        news_f = ''
        for i in range(15):
            news_f = news_f + news[i] + '\n\n'
        await message.channel.send('Вот актуальные новости на сегодня:\n\n' + news_f)

    elif message.content.find('!quote') != -1:
        quote = get_random_guote()
        await message.channel.send('Вот твоя цитата на сегодня:\n\n' + quote)

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == 'основной-канал':
            num = random.randint(0, len(welcome) - 1)
            await channel.send(f'''{welcome[num]}{member.mention}!''')


client.run(token)
