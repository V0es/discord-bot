from typing import List


from python_aternos import Client, AternosServer
from python_aternos import ServerStartError

from aternos.models import User
from aternos.exceptions import NoLoginError, ServerRefreshError, ServerNotExist


from discord import Embed

server_states = {'offline' : 'Оффлайн',
    'loading' : 'Загрузка',
    'starting' : 'Подготовка',
    'online' : 'Онлайн'}

class AtHandler():
    def __init__(self) -> None:
        self.logged_in = False
        
        

    def __del__(self):
        pass


    def login(self, user : User):
        if self.logged_in:
            try:
                self._logout()
            except Exception:
                pass    
            
        try:
            self.client = Client.restore_session(file=f'aternos/sessions/.at_{user.aternos_username}')
        except Exception:
            self.client = Client.from_hashed(user.aternos_username, user.aternos_password, sessions_dir='aternos/sessions')

        self.servers = self.client.list_servers()
        self.at_username = user.aternos_username
        self.logged_in = True
        
        try:
            self.server_ids = [server.servid for server in self.client.list_servers()]
        except Exception:
            self.server_ids = []

    def _logout(self):
        if not self.logged_in:
            raise

        self.client.save_session(file=f'aternos/sessions/.at_{self.at_username}')
        self.client.logout()
        self.logged_in = False


    def get_server_list(self) -> List[AternosServer]:
        self._check_errors()
        return self.server_list
        

    def _refresh_servers(self):
        self.client.refresh_servers(self.server_ids)
        try:
            self.server_list = self.client.list_servers()
        except Exception as e:
            print(e)
            raise ServerRefreshError

    @staticmethod
    def _create_server_embed(server : AternosServer, verbose) -> Embed:
        
        server_embed = Embed(title='Minecraft Server')
        server_embed.add_field(name='Адрес сервера', value=server.address)
        server_embed.add_field(name='Cтатус', value=server_states[server.status])
        
        if verbose:
            server_embed.add_field(name='Платформа', value='Bedrock' if server.is_bedrock else 'Java')
            server_embed.add_field(name='Ядро', value=server.software)
            server_embed.add_field(name='Версия', value=server.version)
            server_embed.add_field(name='Используемая память', value=f'{server.ram} MB')
            if server.status == 'online':
                server_embed.add_field(name='Число игроков', value=f'{server.players_count}/{server.slots}')

                if server.players_count:
                    players_msg = ''
                    for id, player in enumerate(server.players_list):
                        players_msg += f'{id+1}) {player}\n'
                    server_embed.add_field(name='Список игроков', value=players_msg)

        return server_embed


    def _check_errors(self):
        if not self.logged_in:
            raise NoLoginError
        try:
            self._refresh_servers()
        except ServerRefreshError:
            raise ServerRefreshError


    def start_server(self, server_index: int):
        self._check_errors()
        try:
            server_to_start = self.server_list[server_index - 1]
        except IndexError:
            raise ServerNotExist
        
        try:
            server_to_start.start()
        except ServerStartError:
            raise ServerStartError


    def server_info(self, server_index : int, verbose : bool = False):
        self._check_errors()
        
        try:
            server = self.server_list[server_index - 1]
        except IndexError:
            raise ServerNotExist

        server_embed = self._create_server_embed(server, verbose)

        return server_embed
        

