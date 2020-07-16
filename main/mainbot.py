import discord
import random
import pyowm
import requests

status_dict = {
    'clouds': 'облачно',
    'rain': 'дождь',
    'clear': 'ясно',
    'haze': 'туман', }
greetings = ['Салам, ', 'Здарова, ', 'Чо каво, сучара. Это мой кореш ', 'Давно не виделись, ', 'Здравствуй, ',
             'И тебе не хворать, ', 'Мы же с тобой уже сегодня виделись, ', 'Привет, ',
             'Ебать, божнур,  ', 'Как же ты меня уже заебал, ', 'Всем хай! И тебе, ']
welcome = ['Вот это да! Кто пожаловал! Это ', 'Добро пожаловать на сервер, ', 'Ой! Кто-то новенький! К нам зашёл ']
localTimeFormat = "%H:%M:%S %d-%m-%Y"

pyowm_api_key = 'b79bb697bf0d4dacdaa4e6969c13040d'
yandex_api_key = '593de6af-0e94-4ec9-a34a-c58933c2c20d'
token = 'Njk2NTQ0NTgyNzQxMTMxMjc0.XvH6Pg._k5Oi2JjhEKUcLzXuvoiht-8Rjw'
request_url = 'https://api.weather.yandex.ru/v2/forecast/'

owm = pyowm.OWM(pyowm_api_key, language='ru')

client = discord.Client()


def get_suntime_info(paramspack, headerspack):
    """Данная функция формирует и отправляет GET запрос на сервер на основе полученных параметров,
                    ответ преобразует к удобному для работы виду и возвращает его"""

    answer = requests.get(request_url, params=paramspack,
                          headers=headerspack).json()  # формирую get запрос, ответ перевожу в json
    answer = list(answer['forecasts'][
                      0].items())  # беру dict_list всех пар словаря answer и преобразую в list для дальнейшей работы
    suntimes = dict([answer[0], answer[3], answer[4], answer[5],
                     answer[6]])  # 'выдёргиваю' из списка нужные пары и складываю новый словарь
    suntimes['date'] = swap_year_day(suntimes['date'])
    return suntimes


def swap_year_day(date):
    """Данная функция приводит дату к более читабельному виду
                (из формата YYYY-MM-DD преобразует в формат DD.MM.YYYY)
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


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    id = client.get_guild(394165433797836801)

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
        await message.channel.send(embed=embd)

    elif message.content.find('!members') != -1:
        members = id.member_count
        await message.channel.send(f'''На сервере {members} участников.''')

    elif message.content.find('!weather') != -1:
        city = message.content[9::]
        print(city)
        try:
            observation = owm.weather_at_place(city)
        except pyowm.exceptions.api_response_error.NotFoundError:
            await message.channel.send('Я не знаю такого города :(')
            return

        weather = observation.get_weather()
        temperature = weather.get_temperature('celsius')
        wind = weather.get_wind('meters_sec')
        hum = weather.get_humidity()
        status = weather.get_status()
        pressure = weather.get_pressure()
        pressure = round(pressure['press'] * 0.750062, 1)

        await message.channel.send(
            f'''В городе {city} сейчас {status_dict[str(status).lower()]}. 
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


@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == 'основной-канал':
            num = random.randint(0, len(welcome) - 1)
            await channel.send(f'''{welcome[num]}{member.mention}!''')


client.run(token)
