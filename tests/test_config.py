import pytest
from environs import Env

from src.config import load_config


@pytest.fixture
def env_test() -> Env:
    env = Env()
    env.read_env()
    return env


def test_config(env_test: Env) -> None:
    config = load_config()
    assert int(env_test("API_ID")) == config.user_bot.api_id
    assert env_test("API_HASH") == config.user_bot.api_hash
    assert env_test("DB_HOST") == config.data_base.host
    assert int(env_test("DB_PORT")) == config.data_base.port
    assert env_test("DB_USER") == config.data_base.user
    assert env_test("DB_PASS") == config.data_base.password
    assert env_test("DB_NAME") == config.data_base.db_name
