import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    DB_NAME: str
    DB_PASS: str
    DB_LOGIN: str
    DB_HOST: str
    DB_PORT: str
    DB_URL: str


def _init_config():
    load_dotenv()
    return Settings(DB_NAME=os.getenv("DB_NAME"),
                    DB_PASS=os.getenv("DB_PASS"),
                    DB_LOGIN=os.getenv("DB_LOGIN"),
                    DB_HOST=os.getenv("DB_HOST"),
                    DB_PORT=os.getenv("DB_PORT"),
                    DB_URL=os.getenv("DB_URL"))


logging.basicConfig(level=logging.DEBUG)




config = _init_config()
if __name__ == '__main__':
    print(config)
