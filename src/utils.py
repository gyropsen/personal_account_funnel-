import asyncio
from datetime import datetime

from pyrogram import Client

from src.manager import ObjectiveMessagesDBManager, UserDBManager
from src.models import ObjectiveMessage, Status, Users

user_manager = UserDBManager()
messages_manager = ObjectiveMessagesDBManager()


async def check_trigger(message: str | None) -> bool | None:
    """
    Проверка на слово-триггер
    :param message: str | None
    :return: bool | None
    """
    if message:
        return message.strip().lower() == "прекрасно" or message.strip().lower() == "ожидать"


async def get_user(user_telegram_id: str) -> Users | None:
    """
    Проверка пользователя по наличию и статусу
    :param user_telegram_id: str
    :return: Users | None
    """
    user_from_db = await user_manager.select_user_by_telegram_id(user_telegram_id)

    # Если пользователя нет в бд
    if not user_from_db:
        # то создать
        await user_manager.insert_user({"telegram_id": user_telegram_id, "status": Status.alive})
        user_from_db = await user_manager.select_user_by_telegram_id(user_telegram_id)

    # иначе, если у пользователя статус finished или dead
    if user_from_db[0].status in [Status.finished, Status.dead]:
        # то вернуть None
        return

    # Иначе вернуть пользователя
    return user_from_db[0]


async def write_message(client: Client, user: Users, text: str):
    """
    Функция отправки пользователю сообщения
    :param client: Client
    :param user: Users
    :param text: str
    :return: None
    """
    try:
        await client.send_message(chat_id=user.telegram_id, text=text)
    except Exception as error:
        print(error)
        await user_manager.update_status_user(user.id, Status.dead)


async def send_messages(app: Client, message: ObjectiveMessage):
    """
    Функция планирования отправки сообщений
    :param app: Client
    :param message: ObjectiveMessage
    :return: None
    """
    # Обновить задачу на стоп - значит, что функция начала работу, но еще не выполнена
    await messages_manager.update_stop(message.id, True)

    # Получить пользователя
    user = await user_manager.select_user_by_id(message.user_id)

    # Если ранее пользователь создан
    if user:
        # то запускаем задачи
        for message_for_write, message_timeout in {
            message.text_1: message.timeout_1,
            message.text_2: message.timeout_2,
            message.text_3: message.timeout_3,
        }.items():
            write_user = await user_manager.select_user_by_id(message.user_id)
            print(write_user[0].status)
            if write_user[0].status != Status.finished:
                while True:
                    if datetime.now() - write_user[0].updated_at >= message_timeout:
                        print(message_for_write)
                        await write_message(app, write_user[0], message_for_write)
                        await user_manager.update_updated_at(write_user[0].id, datetime.now())
                        break
                # иначе пропускать задачу
        # После исполнения всех задач присвоить пользователю статус finished
        await user_manager.update_status_user(user[0].id, Status.finished)
    else:
        # иначе ничего
        print("finish!")

    # Удалить задачу
    await messages_manager.delete_objective_message(message.id)


async def start_scheduler(app):
    print("start_scheduler")

    while True:
        # Проверять наличие новых задач
        objectives_message = await messages_manager.select_objective_messages_filter_stop_false()
        tasks = [asyncio.create_task(send_messages(app, obj_message)) for obj_message in objectives_message]
        await asyncio.gather(*tasks)
