from dataclasses import dataclass

from environs import Env


@dataclass
class UserBot:
    api_id: int
    api_hash: str


@dataclass
class DataBase:
    host: str
    port: int
    user: str
    password: int
    db_name: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    @property
    def database_url_psycopg(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass
class Config:
    user_bot: UserBot
    data_base: DataBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        user_bot=UserBot(api_id=int(env("API_ID")), api_hash=env("API_HASH")),
        data_base=DataBase(
            host=env("DB_HOST"),
            port=int(env("DB_PORT")),
            user=env("DB_USER"),
            password=env("DB_PASS"),
            db_name=env("DB_NAME"),
        ),
    )
