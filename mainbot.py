#Importing built-in libs
import random
import io

#Importing third-party libs
import discord


#Importing project files 
from config import Config as cfg
import weather
from command import Command
import web
import news
from pictures import Picture

client = discord.Client()


#TODO: change every message parsing into a function call

greetings = ['Салам, ', 'Здарова, ', 'Чо каво, сучара. Это мой кореш ', 'Давно не виделись, ', 'Здравствуй, ',
             'И тебе не хворать, ', 'Мы же с тобой уже сегодня виделись, ', 'Привет, ',
             'Ебать, божнур,  ', 'Как же ты меня уже заебал, ', 'Всем хай! И тебе, ']
welcome = ['Вот это да! Кто пожаловал! Это ', 'Добро пожаловать на сервер, ', 'Ой! Кто-то новенький! К нам зашёл ']


localTimeFormat = "%H:%M:%S %d-%m-%Y"





@client.event
async def on_message(message):
    command = Command(message)

    if command.author == client.user:
        return


    dis_id = client.get_guild(int(cfg.guild_id))


    if command.command == '!hello':
        num = random.randint(0, len(greetings) - 1)
        await message.channel.send(f'''{greetings[num]}{message.author.name}!''')


    elif command.command == '!help':
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


    elif command.command == '!members':
        members = dis_id.member_count
        await message.channel.send(f'''На сервере {members} участников.''')


    elif command.command == '!weather':
        city = command.args
        weather_message = weather.get_weather_status(city)
        
        await message.channel.send(weather_message)


    elif command.command == '!suntime':
        city = command.args
        suntime_message = weather.get_suntime_status(city)

        await message.channel.send(suntime_message)


    elif command.command == '!pic':
        keyword = command.args
        
        picture = Picture(keyword)
        dis_file = discord.File(fp=io.BytesIO(picture.picture_binary), filename=picture.pic_path)
        await message.channel.send(file=dis_file)
        await picture.delete()

    elif command.command == '!news':
        """Вывод последних 15 новостей из списка актуальных"""
        news_str = news.get_news()
        
        await message.channel.send('Вот актуальные новости на сегодня:\n\n' + news_str)


    elif command.command == '!quote':
        """Вывод случайной цитаты"""
        quote = web.get_random_guote()
        await message.channel.send('Вот твоя цитата на сегодня:\n\n' + quote)

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == 'основной-канал':
            num = random.randint(0, len(welcome) - 1)
            await channel.send(f'''{welcome[num]}{member.mention}!''')


client.run(cfg.bot_token)


