from python_aternos import Client, AternosServer
from typing import List

class AtHandler():
    def __init__(self) -> None:
        try:
            self.client = Client.restore_session(file='C:/Users/markk/VSCode Projects/discord-bot/discord-bot/aternos/sessions/.at_v0es_test')
            print('Successfully restored session')
        except FileNotFoundError:
            print('Session file not found. Trying to log in with credentials...')
            self.client = Client.from_credentials('v0es_test', 'yadebililoh', sessions_dir="C:/Users/markk/VSCode Projects/discord-bot/discord-bot/aternos/sessions")
        print(self.client)    


    def start_server(self, server_ip : str):
        servers = self.get_server_list()
        for server in servers:
            if server.address == server_ip:
                server_to_start = server
        server.start()

    def get_server_list(self) -> List[AternosServer]:
        return self.client.list_servers()

    def server_info(self, server_ip : str):
        for server in self.get_server_list():
            print(server)
            if server.address == server_ip:
                serv = server
        return {'server_address' : serv.address,
                'server_status'  : serv.css_class}
        


aternos = AtHandler()
servers = aternos.get_server_list()
for serv in servers:
    print(serv.address, aternos.server_info(serv.address))

server_addr = input('Enter address to start: ')
aternos.start_server(server_addr)



