from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_id: list


@dataclass
class Config:
    tgbot: TgBot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    admin_id = list(map(int, env("ADMIN_ID").split(',')))
    return Config(tgbot=TgBot(token=env("BOT_TOKEN"), admin_id=admin_id))
