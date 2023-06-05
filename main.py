import threading
import time

from database.database import DataBaseManager
from handler import Handler
from bot.bot import CryptoArbitrageBot
from config import token, dbname, user, password, host, port


def start_handler():
    db = DataBaseManager(dbname=dbname, user=user, password=password, host=host, port=port)
    handler = Handler(db)
    while True:
        handler.handle()
        time.sleep(30)


def main():
    thread = threading.Thread(target=start_handler)
    thread.daemon = True
    thread.start()

    bot = CryptoArbitrageBot(token)
    bot.start()


if __name__ == '__main__':
    main()
