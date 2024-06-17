from pyrogram import filters
from pyrogram.handlers import MessageHandler

from src.manager import ObjectiveMessagesDBManager, UserDBManager
from src.models import Status
from src.utils import check_trigger, get_user

message_manager = ObjectiveMessagesDBManager()
user_manager = UserDBManager()


async def check_alive(client, message):
    """
    Обработчик слов-триггеров от юзербота
    """
    # Если в сообщениях есть слова триггеры, то присвоить статус finish
    messages = [
        await check_trigger(mess.text)
        async for mess in client.get_chat_history(message.chat.id, limit=5)
        if mess.from_user.is_self
    ]
    user = await get_user(str(message.from_user.id))
    if user:
        if True in messages:
            await user_manager.update_status_user(user.id, Status.finished)


async def message_private_handler(client, message):
    """
    Обработчик слов-триггеров от пользователя
    """
    # Получить от пользователя сообщение и создать задачу.
    # Проверить статус User | None
    user = await get_user(str(message.from_user.id))
    await message_manager.insert_objective_message({"user": user})


check_alive_handler = MessageHandler(check_alive, filters=(filters.me & filters.private))
user_handler = MessageHandler(message_private_handler, filters=filters.private)
