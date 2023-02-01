#Importing built-in libs
import random
import io
import asyncio
import logging

#Importing third-party libs
import discord
from python_aternos import AternosServer


#Importing project files 
from config import Config as cfg
import weather
from command import Command
import web
import news
from pictures import Picture

from aternos.aternos_handler import AtHandler
from aternos.models import Database, User



db = Database(db_path=cfg.database_path)
aternos = AtHandler()
discord.utils.setup_logging(level=logging.INFO)


greetings = ['Салам, ', 'Здарова, ', 'Чо каво, сучара. Это мой кореш ', 'Давно не виделись, ', 'Здравствуй, ',
             'И тебе не хворать, ', 'Мы же с тобой уже сегодня виделись, ', 'Привет, ',
             'Ебать, божнур,  ', 'Как же ты меня уже заебал, ', 'Всем хай! И тебе, ']
welcome = ['Вот это да! Кто пожаловал! Это ', 'Добро пожаловать на сервер, ', 'Ой! Кто-то новенький! К нам зашёл ']

server_classes = {'offline' : 'Оффлайн',
    'loading' : 'Загрузка',
    'preparing' : 'Подготовка',
    'online' : 'Онлайн'}


class DiscordBot(discord.Client):
    async def on_ready(self):
        print(f'Logged as {self.user}. ID: {self.user.id}')
    

    async def on_message(self, message):
        command = Command(message)

        if command.author.id == self.user.id:
            return


        dis_id = self.get_guild(int(cfg.guild_id))


        if command.command == '!hello':
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


        elif command.command == '!at_signup':
            """Регистрация своего аккаунта Aternos"""
            user = command.author
            await user.send(f'''Привет, {user.name}!\n
            В этом диалоге можно настроить Aternos-сервис, чтобы тебе больше не приходилось вручную запускать сервер по просьбе друзей\n
            Я могу запускать нужный сервер всего в пару команд, круто, правда?\n
            Так вот, для начала придумай себе имя пользователя\n
            По нему другие пользователи будут выбирать твой аккаунт и запускать сервера, так что выбери такой юзернейм, по которому тебя уже знают друзья''')

            def check(m : discord.Message) -> bool:
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
                
                
                db.add_user(User(public_username, aternos_username, aternos_password))

                await user.send(f'Супер, твой аккаунт Aternos теперь привязан к боту!')

                await user.send(f'Логин: {aternos_username}\nПароль: {aternos_password}')
                
            except asyncio.TimeoutError:
                await user.send(f'''Что-то ты долго мне не отвечаешь :(\n
                Наверное, ты уснул. Напиши мне ещё раз как освободишься...''')
                return


        elif command.command == '!at_login':
            """Выбор аккаунта Aternos, привязанного к боту
            chech - функция проверки валидности сообщения"""

           
            def check(m : discord.Message) -> bool:
                return m.author == message.author and m.channel == message.channel and m.content in public_usernames

            users = db.get_all_users()

            if len(users) == 0: #если в бд нет записей
                await message.channel.send(f'У вас не привязано ни одного аккаунта Aternos :( Воспользуйтесь командой **!aternos_signup** и я помогу вам это исправить!')
                return

            elif len(users) == 1: #если в бд одна запись => выбирать акк не нужно
                aternos_user = users[0]
                await message.channel.send(f'Выбран единственный привязанный аккаунт Aternos - {aternos_user.public_username}')
                

            else: # если записей больше 1
                public_usernames = [user.public_username for user in users] # список публичных юзернеймов всех записей
                username_msg = ''

                for i, username in enumerate(public_usernames): # формируем сообщение для выбора аккаунта
                    username_msg += f'{i + 1}) {username}\n' 
                await message.channel.send(f'У вас привязано несколько аккаунтов Aternos. Выберете, какой вам нужен:\n' + username_msg)

                try:
                    chosen_username = await self.wait_for('message', check=check, timeout=15*60.0) # пользователь вводит имя аккаунта, под которым хочет залогиниться

                except asyncio.TimeoutError:
                    await message.channel.send(f'Вы, по всей видимости, забыли выбрать аккаунт. За такое неуважение вам придётся вводить команду заново!')
                    return

                aternos_user = list(filter(lambda usr: usr.public_username == chosen_username, users))[0] # фильтруем записи по публичному юзернейму, который ввёл пользователь и выбираем первую(и единственную)
                await message.channel.send(f'Отлично, вы выбрали аккаунт: *{chosen_username}*')

            aternos.login(aternos_user) # логинимся в атернос под выбранным аккаунтом


        elif command.command == '!at_servers':
            '''Получить список серверов аккаунта, под которым был выполнен вход'''

            servers = aternos.get_server_list()

            if not servers:
                await message.channel.send('Не удалось получить список серверов :(')
                return
            elif not len(servers):
                await message.channel.send('Жесть, на вашем аккаунте нет ни одного сервера...')
                return

            
            for id, server in enumerate(servers):
                #print(server)
                server_embed = self.create_server_embed(server)
                await message.channel.send(f'Сервер #{id+1}', embed=server_embed)
            
        elif command.command == '!server_info':
            server_index = command.args

        

    @staticmethod
    def create_server_embed(server : AternosServer, verbose=False) -> discord.Embed:
        server_embed = discord.Embed(
            title='Minecraft Server',
            description=server.address)
        server_embed.add_field(name='Адрес сервера', value=server.address)
        server_embed.add_field(name='Cтатус', value=server_classes[server.status])
        return server_embed

    async def on_member_join(member):
        for channel in member.guild.channels:
            if str(channel) == 'основной-канал':
                num = random.randint(0, len(welcome) - 1)
                await channel.send(f'''{welcome[num]}{member.mention}!''')






intents = discord.Intents.all()


client = DiscordBot(intents=intents)
client.run(cfg.bot_token)


