import enum
from datetime import datetime, timedelta
from typing import Annotated

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

created_at = Annotated[datetime, mapped_column(default=datetime.now())]
updated_at = Annotated[datetime, mapped_column(default=datetime.now())]


# Создание декларативной базы
class Base(DeclarativeBase):
    pass


# Выбор статуса
class Status(enum.Enum):
    alive = "alive"
    dead = "dead"
    finished = "finished"


#  Модели бд
class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[str]
    created_at: Mapped[created_at]
    status: Mapped[Status]
    updated_at: Mapped[updated_at]


class ObjectiveMessage(Base):
    __tablename__ = "objective_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[created_at]
    text_1: Mapped[str] = mapped_column(default="message_1")
    text_2: Mapped[str] = mapped_column(default="message_2")
    text_3: Mapped[str] = mapped_column(default="message_3")

    timeout_1: Mapped[timedelta] = mapped_column(default=timedelta(seconds=20))
    timeout_2: Mapped[timedelta] = mapped_column(default=timedelta(seconds=30))
    timeout_3: Mapped[timedelta] = mapped_column(default=timedelta(seconds=40))

    stop: Mapped[bool] = mapped_column(default=False)

    user_id = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("Users", foreign_keys=[user_id])
