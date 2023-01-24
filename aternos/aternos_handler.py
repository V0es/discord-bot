from python_aternos import Client
from command import Command
from config import Config as cfg


class AtHandler():
    def __init__(self) -> None:
        
        self.client = Client.restore_session()
        if not self.client:
            self.client = Client.from_credentials(cfg.at_usrname, cfg.at_pass, sessions_dir='/sessions')

        self.command = cmd
    

    def __del__(self):
        self.client.save_session()

    def start_server(server_id : str):
        pass

    @staticmethod
    def get_server_list():
        self.client  

    def server_info(server_id : str):
        pass

