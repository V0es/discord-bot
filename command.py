class Command:

    def __init__(self, message) -> None:
        self.command = self._parse_command(message)
        self.args = self._parse_args(message, len(self.command))
        self.author = message.author


    @staticmethod
    def _parse_command(message : str) -> str:
        """Парсит сам текст команды"""
        command = message.content.split(' ')[0]
        return command


    @staticmethod
    def _parse_args(message : str, com_length : int) -> str:
        """Парсит аргументы команды"""
        return message.content[com_length + 1::]

           