from python_aternos import Client, AternosServer
from command import Command
from config import Config as cfg


class AtHandler():
    def __init__(self, name) -> None:
        self.name = name
        try:
            self.client = Client.restore_session(file=f'aternos/sessions/{name}.aternos')
        except Exception:
            self.username = cfg.at_usrname
            self.password_hash = cfg.at_pass_hashed
            self.client = Client.from_hashed(self.username, self.password_hash, sessions_dir='aternos/sessions')
            

    def __del__(self):
        self.client.save_session(file=f'aternos/sessions/{self.name}.aternos')

    

    def start_server(server_id : str):
        pass

    def get_server_list():
        self.client  

    def server_info(server_id : str):
        pass

