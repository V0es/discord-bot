#Importing built-in libs
import random

greetings = ['Салам, ', 'Здарова, ', 'Чо каво, сучара. Это мой кореш ', 'Давно не виделись, ', 'Здравствуй, ',
             'И тебе не хворать, ', 'Мы же с тобой уже сегодня виделись, ', 'Привет, ',
             'Ебать, божнур,  ', 'Как же ты меня уже заебал, ', 'Всем хай! И тебе, ']
welcome = ['Вот это да! Кто пожаловал! Это ', 'Добро пожаловать на сервер, ', 'Ой! Кто-то новенький! К нам зашёл ']


pyowm_api_key = 'b79bb697bf0d4dacdaa4e6969c13040d'
yandex_api_key = '593de6af-0e94-4ec9-a34a-c58933c2c20d'
token = 'Njk2NTQ0NTgyNzQxMTMxMjc0.XvH6Pg._k5Oi2JjhEKUcLzXuvoiht-8Rjw'
request_url = 'https://api.weather.yandex.ru/v2/forecast/'

owm = pyowm.OWM(pyowm_api_key, language='ru')






def get_suntime_info(paramspack, headerspack):

    """Данная функция формирует и отправляет GET запрос на сервер на основе полученных параметров,
                    ответ преобразует к удобному для работы виду и возвращает его"""

    answer = requests.get(request_url, params=paramspack, headers=headerspack).json()  # формирую get запрос, ответ перевожу в json
    answer = list(answer['forecasts'][0].items())  # беру dict_list всех пар словаря answer и преобразую в list для дальнейшей работы
    print(answer)
    suntimes = dict([answer[0], answer[3], answer[4], answer[5], answer[6]])  # 'выдёргиваю' из списка нужные пары и складываю новый словарь
    suntimes['date'] = swap_year_day(suntimes['date'])
    return suntimes


def swap_year_day(date):

    """Данная функция приводит дату к более читабельному виду
                (из формата YYYY-MM-DD преобразует в формат DD.MM.YYYY)"""

    date = date.split('-')
    tmp = date[0]
    date[0] = date[2]
    date[2] = tmp
    date = '-'.join(date)
    return date


@client.event
async def on_message(message):
    command = Command(message)

    if command.author == client.user:
        return


    dis_id = client.get_guild(int(cfg.guild_id))


    if command.command == '!hello':
        num = random.randint(0, len(greetings) - 1)
        await message.channel.send(f'''{greetings[num]}{message.author.name}!''')


        embd = discord.Embed(title='Доступные команды', description='')
        embd.add_field(name='!help', value='Справка по доступным командам')
        embd.add_field(name='!members', value='Количество пользователей на сервере')
        embd.add_field(name='!hello', value='Приветствие пользователя')
        embd.add_field(name='!weather <город>', value='Показывает погоду в указанном городе')
        embd.add_field(name='!suntime <город>', value='Показывает время восхода/захода солнца в указанном городе')


@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == 'основной-канал':
            num = random.randint(0, len(welcome) - 1)
            await channel.send(f'''{welcome[num]}{member.mention}!''')



