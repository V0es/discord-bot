#Importing built-in libs
import random
import io
import asyncio

#Importing third-party libs
import discord


#Importing project files 
from config import Config as cfg
import weather
from command import Command
import web
import news
from pictures import Picture

from aternos import models



#TODO: change every message parsing into a function call

greetings = ['Салам, ', 'Здарова, ', 'Чо каво, сучара. Это мой кореш ', 'Давно не виделись, ', 'Здравствуй, ',
             'И тебе не хворать, ', 'Мы же с тобой уже сегодня виделись, ', 'Привет, ',
             'Ебать, божнур,  ', 'Как же ты меня уже заебал, ', 'Всем хай! И тебе, ']
welcome = ['Вот это да! Кто пожаловал! Это ', 'Добро пожаловать на сервер, ', 'Ой! Кто-то новенький! К нам зашёл ']




class DiscordBot(discord.Client):
    async def on_ready(self):
        print(f'Logged as {self.user}. ID: {self.user.id}')
    

    async def on_message(self, message):
        command = Command(message)

        if command.author.id == self.user.id:
            return


        dis_id = self.get_guild(int(cfg.guild_id))


        if message.content.startswith('!hello'):
            num = random.randint(0, len(greetings) - 1)
            await message.reply(f'''{greetings[num]}{message.author.name}!''', mention_author=True)


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

            try:
                await picture.delete()
            except FileNotFoundError:
                pass


        elif command.command == '!news':
            """Вывод последних 15 новостей из списка актуальных"""
            news_str = news.get_news()

            await message.channel.send('Вот актуальные новости на сегодня:\n\n' + news_str)


        elif command.command == '!quote':
            """Вывод случайной цитаты"""
            quote = web.get_random_guote()
            await message.channel.send('Вот твоя цитата на сегодня:\n\n' + quote)


        elif command.command == '!aternos_signup':
            """Регистрация своего аккаунта Aternos"""
            user = message.author
            await user.send(f'''Привет, {user.name}!\n
            В этом диалоге можно настроить Aternos-сервис, чтобы тебе больше не приходилось вручную запускать сервер по просьбе друзей\n
            Я могу запускать нужный сервер всего в пару команд, круто, правда?\n
            Так вот, для начала придумай себе имя пользователя\n
            По нему другие пользователи будут выбирать твой аккаунт и запускать сервера, так что выбери такой юзернейм, по которому тебя уже знают друзья''')

            def check(m):
                return m.author == user and isinstance(m.channel, discord.DMChannel)
            
            try:
                public_username = await self.wait_for('message', timeout=5*60.0, check=check)
                public_username = public_username.content
                await user.send(f'{public_username} - отличный выбор! Теперь мне нужно узнать твоё имя пользователя на Aternos')

                aternos_username = await self.wait_for('message', timeout=5*60.0, check=check)
                aternos_username = aternos_username.content
                await user.send(f'Хорошо, теперь введи свой пароль от Aternos')

                aternos_password = await self.wait_for('message', timeout=5*60.0, check=check)
                aternos_password = aternos_password.content
                await user.send(f'Супер, твой аккаунт Aternos теперь привязан к боту!')

                await user.send(f'Логин: {aternos_username}\nПароль: {aternos_password}')
            except asyncio.TimeoutError:
                await user.send(f'''Что-то ты долго мне не отвечаешь :(\n
                Наверное, ты уснул. Напиши мне ещё раз как освободишься...''')
                return

            




    async def on_member_join(member):
        for channel in member.guild.channels:
            if str(channel) == 'основной-канал':
                num = random.randint(0, len(welcome) - 1)
                await channel.send(f'''{welcome[num]}{member.mention}!''')






intents = discord.Intents.default()
intents.messages = True

client = DiscordBot(intents=intents)
client.run(cfg.bot_token)


