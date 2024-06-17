import asyncio
import datetime

from sqlalchemy import delete, select, text

from src.database import async_engine, async_session_factory
from src.models import Base, ObjectiveMessage, Status, Users


class Database:
    async def create_new_tables(self):
        async with async_engine.begin() as conn:
            if not await self.exists_tables():
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @staticmethod
    async def exists_tables() -> list:
        async with async_engine.begin() as conn:
            result = await conn.execute(text("""SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='users'"""))
            table = result.all()
            return table


class UserDBManager:
    @staticmethod
    async def insert_user(new_user: dict):
        async with async_session_factory() as session:
            user = Users(telegram_id=new_user["telegram_id"], status=new_user["status"])
            session.add_all([user])
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_users():
        async with async_session_factory() as session:
            statement = select(Users)
            result = await session.execute(statement)
            users = result.scalars().all()
            return users

    @staticmethod
    async def select_user_by_telegram_id(telegram_id: str) -> list[Users]:
        async with async_session_factory() as session:
            statement = select(Users).filter_by(telegram_id=telegram_id)
            result = await session.execute(statement)
            user_obj = result.scalars().all()
            return user_obj

    @staticmethod
    async def select_user_by_id(_id: int) -> list[Users]:
        async with async_session_factory() as session:
            statement = select(Users).filter_by(id=_id)
            result = await session.execute(statement)
            user_obj = result.scalars().all()
            return user_obj

    @staticmethod
    async def update_status_user(_id: int, new_status: Status):
        async with async_session_factory() as session:
            user = await session.get(Users, _id)
            user.status = new_status
            await session.commit()

    @staticmethod
    async def update_updated_at(_id: int, new_updated_at: datetime):
        async with async_session_factory() as session:
            user = await session.get(Users, _id)
            user.updated_at = new_updated_at
            await session.commit()


class ObjectiveMessagesDBManager:
    @staticmethod
    async def select_objective_messages():
        async with async_session_factory() as session:
            statement = select(ObjectiveMessage)
            result = await session.execute(statement)
            objectives_message = result.scalars().all()
            return objectives_message

    @staticmethod
    async def select_objective_messages_filter_stop_false():
        async with async_session_factory() as session:
            statement = select(ObjectiveMessage).filter_by(stop=False)
            result = await session.execute(statement)
            objectives_message = result.scalars().all()
            return objectives_message

    @staticmethod
    async def select_objective_messages_filter_stop_true():
        async with async_session_factory() as session:
            statement = select(ObjectiveMessage).filter_by(stop=True)
            result = await session.execute(statement)
            objectives_message = result.scalars().all()
            return objectives_message

    @staticmethod
    async def insert_objective_message(new_objective: dict):
        async with async_session_factory() as session:
            objective_message = ObjectiveMessage(
                user=new_objective["user"],
            )
            session.add_all([objective_message])
            await session.flush()
            await session.commit()

    @staticmethod
    async def delete_objective_message(_id: int):
        print("delete_objective_message")
        async with async_session_factory() as session:
            statement = delete(ObjectiveMessage).filter_by(id=_id)
            await session.execute(statement)
            await session.commit()

    @staticmethod
    async def update_stop(_id: int, stop: bool):
        async with async_session_factory() as session:
            user = await session.get(ObjectiveMessage, _id)
            user.stop = stop
            await session.commit()


async def main():
    # pass
    # manager = Database()
    # await manager.drop_tables()
    # await manager.create_new_tables()
    # manager_messages = ObjectiveMessagesDBManager()
    user_manager = UserDBManager()
    # await user_manager.insert_user({"telegram_id": "01234", "status": Status.alive})
    users = await user_manager.select_users()
    #
    for user in users:
        print(user.status, user.telegram_id)
    #     await user_manager.update_status_user(user.id, Status.finished)
    #
    # new_users = await user_manager.select_users()
    # for new_user in new_users:
    #     print(new_user.status, new_user.telegram_id)

    # messages = await manager_messages.select_objective_messages()
    # print(messages)
    # for mess in messages:
    #     print(mess.stop)
    # print(users)
    # user = await user_manager.select_user_by_telegram_id("01234")
    # print(user[0].id)
    # await manager_messages.insert_objective_message(
    #     {"time_start": datetime.datetime.now(), "text": "text1", "timeout": datetime.timedelta(seconds=5),
    #      "user": user[0]})
    # messages = await manager_messages.select_objective_messages()
    # print(messages[0].user_id)
    # await manager_messages.delete_objective_message(messages[0].id)
    # messages = await manager_messages.select_objective_messages()
    # print(messages)

    # await manager_messages.insert_objective_message(
    #     {"time_start": datetime.datetime.now(), "text": "text1", "timeout": datetime.timedelta(seconds=5)})
    # print(await manager_messages.select_objective_messages())
    # for message in await manager_messages.select_objective_messages():
    #     print(message.text, message.timeout, type(message.timeout))


if __name__ == "__main__":
    asyncio.run(main())
