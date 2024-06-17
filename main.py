import asyncio

from pyrogram import Client, compose

from src.config import load_config
from src.handlers import check_alive_handler, user_handler
from src.manager import Database, ObjectiveMessagesDBManager
from src.utils import start_scheduler

config = load_config()
database = Database()
manager_messages = ObjectiveMessagesDBManager()


async def main():
    """
    Конфигурация и старт
    :return:
    """
    # Если не создана бд, то создать её
    await database.create_new_tables()

    # Получить app, добавить обработчики
    app = Client("my_account", api_id=config.user_bot.api_id, api_hash=config.user_bot.api_hash)
    app.add_handler(check_alive_handler)
    app.add_handler(user_handler)
    tasks = [start_scheduler(app), compose([app])]

    # Запустить обработчики и планировщик
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
