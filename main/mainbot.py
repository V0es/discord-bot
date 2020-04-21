import discord
import random
import pyowm


status_dict = {
    'clouds': 'облачно',
    'rain': 'дождь',
    'clear': 'ясно',

}
api_key = 'b79bb697bf0d4dacdaa4e6969c13040d'
token = 'Njk2NTQ0NTgyNzQxMTMxMjc0.XoqSCg.CVq2nnpg9H7YnuCsmUbxHRoxHsE'
greetings = ['Салам, ', 'Здарова, ', 'Чо каво, сучара. Это мой кореш ', 'Давно не виделись, ', 'Здравствуй, ',
             'И тебе не хворать, ', 'Мы же с тобой уже сегодня виделись, ', 'Привет, ',
             'Ебать, божнур,  ', 'Как же ты меня уже заебал, ', 'Всем хай! И тебе, ']
welcome = ['Вот это да! Кто пожаловал! Это ', 'Добро пожаловать на сервер, ', 'Ой! Кто-то новенький! К нам зашёл ']
owm = pyowm.OWM(api_key, language='ru')



client = discord.Client()


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
        await message.channel.send(embed=embd)
    elif message.content.find('!members') != -1:
        members = id.member_count
        await message.channel.send(f'''На сервере {members} участников.''')
    elif message.content.find('!weather') != -1:
        city = message.content[9::]
        print(city)
        observation = owm.weather_at_place(city)
        weather = observation.get_weather()
        temperature = weather.get_temperature('celsius')
        wind = weather.get_wind('meters_sec')
        hum = weather.get_humidity()
        status = weather.get_status()
        await message.channel.send(f'''В городе {city} сейчас {status_dict[str(status).lower()]}. Температура: {round(temperature['temp'])}°С. 
        Влажность воздуха: {hum}%. Скорость ветра: {round(wind['speed'])} м/с.''')


@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == 'основной-канал':
            num = random.randint(0, len(welcome) - 1)
            await channel.send(f'''{welcome[num]}{member.mention}!''')



client.run(token)
