from typing import List


from python_aternos import Client, AternosServer
from config import Config as cfg

from aternos.models import User


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
            
        self.servers = self.client.list_servers()
        self.at_username = user.aternos_username

        try:
            self.client = Client.restore_session(file=f'aternos/sessions/.at_{user.aternos_username}')
        except Exception:
            self.client = Client.from_hashed(user.aternos_username, user.aternos_password, sessions_dir='aternos/sessions')

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
        self.client.refresh_servers(self.server_ids)

        try:
            self.server_list = self.client.list_servers()
        except Exception:
            self.servers = None
        return self.server_list
        

    def start_server(server_id : str):
        pass


    def server_info(server_id : str):
        pass

