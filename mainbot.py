#Importing built-in libs
import random
import io
import asyncio
import logging

#Importing third-party libs
import discord
from python_aternos import AternosServer, ServerStartError


#Importing project files 
from config import Config as cfg
import weather
from command import Command
import web
import news
from pictures import Picture

from aternos.aternos_handler import AtHandler
from aternos.models import Database, User
from aternos.exceptions import NoLoginError, ServerRefreshError, ServerNotExist



db = Database(db_path=cfg.database_path)
aternos = AtHandler()
discord.utils.setup_logging(level=logging.INFO)


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
            #TODO: сделать проверку аккаунта на валидность
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
                await message.channel.send(f'У вас не привязано ни одного аккаунта Aternos :( Воспользуйтесь командой **!at_signup** и я помогу вам это исправить!')
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
                
                aternos_user = list(filter(lambda usr: usr.public_username == chosen_username.content, users))[0] # фильтруем записи по публичному юзернейму, который ввёл пользователь и выбираем первую(и единственную)
                
                await message.channel.send(f'Отлично, вы выбрали аккаунт: *{aternos_user.public_username}*')

            aternos.login(aternos_user) # логинимся в атернос под выбранным аккаунтом


        elif command.command == '!at_servers':
            '''Получить список серверов аккаунта, под которым был выполнен вход'''
            try:
                servers = aternos.get_server_list()

            except NoLoginError:
                await message.channel.send('Для начала вам необходимо залогиниться')
                return

            except ServerRefreshError:
                await message.channel.send('Упс... Проблема с доступом к серверам. Повторите попытку чуть позже')
                return

            if not len(servers):
                await message.channel.send('Жесть, на вашем аккаунте нет ни одного сервера...')
                return

            for server_index in range(len(servers)):
                server_embed = aternos.server_info(server_index)
                #TODO: перенести построение embed в метод server_info
                await message.channel.send(f'Сервер #{server_index+1}', embed=server_embed)
            

        elif command.command == '!server_info':
            
            try:
                server_index = int(command.args) - 1
            except ValueError:
                await message.channel.send('Признай, хуйню же написал...')
                return

            try:
                server_embed = aternos.server_info(server_index, verbose=True)
            except NoLoginError:
                await message.channel.send('Для начала вам необходимо залогиниться')
                return
            except ServerRefreshError:
                await message.channel.send('Упс... Проблема с доступом к серверам. Повторите попытку чуть позже')
                return
            except ServerNotExist:
                await message.channel.send('Кажется, вы ввели некорректный номер сервера')
                return
            #TODO: перенести построение embed в метод server_info

            await message.channel.send(embed=server_embed)


        elif command.command == '!server_start':
            
            try:
                server_index = int(command.args)
            except ValueError:
                await message.channel.send('Ну и чё ты высрал...')
                return

            try:
                aternos.start_server(server_index)
            except NoLoginError:
                await message.channel.send('Для начала вам необходимо залогиниться')
                return
            except ServerRefreshError:
                await message.channel.send('Упс... Проблема с доступом к серверам. Повторите попытку чуть позже')
                return
            except ServerNotExist:
                await message.channel.send('Кажется, вы ввели некорректный номер сервера')
                return
            except ServerStartError:
                await message.channel.send('Не удалось запустить сервер =( Повторите попытку позже или обратитесь в поддержку')
                return

            #TODO: сделать отчёт о запущенном сервере на вебсокетах websockets
            #TODO: перенести логику запуска сервера в метод start_server
            await message.channel.send('Сервер будет запущен в ближайшее время =)')

        elif command.command == '!roll':
            bounds = command.args
            if not bounds:
                lower_bound, upper_bound = 0, 100
                rand_num = random.randint(lower_bound, upper_bound)
            else:
                bounds = bounds.split('-')
                try:
                    lower_bound, upper_bound = int(bounds[0]), int(bounds[1])
                except Exception:
                    await message.channel.send('Это же надо додуматься такую ебалу написать')
                    return

                try:
                    rand_num = random.randint(lower_bound, upper_bound)
                except ValueError:
                    await message.channel.send('Ты порядок чисел в рот ебал?')
                    return

            await message.channel.send(f'Ваше случайное число от *{lower_bound}* до *{upper_bound}*: **{rand_num}**')
            


    @staticmethod
    def create_server_embed(server : AternosServer, verbose : bool = False) -> discord.Embed:
        pass
        


    async def on_member_join(member):
        for channel in member.guild.channels:
            if str(channel) == 'основной-канал':
                num = random.randint(0, len(welcome) - 1)
                await channel.send(f'''{welcome[num]}{member.mention}!''')


intents = discord.Intents.all()


client = DiscordBot(intents=intents)
client.run(cfg.bot_token)


