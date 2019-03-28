import logging
import logging.config

from src.bot import Bot
from src import config


logging.config.dictConfig(config["logging"])
logger = logging.getLogger("ircstarr")


if __name__ == "__main__":
    logger.info("Starting up")
    bot = Bot(config)
    bot.run_forever()

