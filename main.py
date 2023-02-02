from bot import DiscordBot
from discord import Intents
from config.config import Config as cfg


if __name__ == '__main__':
    intents = Intents.all()

    client = DiscordBot(intents=intents)
    client.run(cfg.bot_token)
