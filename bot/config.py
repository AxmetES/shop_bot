import os

from environs import Env

env = Env()
env.read_env()


class Settings:
    def __init__(self):
        self.BOT_TOKEN = env.str("BOT_TOKEN")
        self.POSTGRES_DB = env.str("POSTGRES_DB")
        self.POSTGRES_USER = env.str("POSTGRES_USER")
        self.POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
        self.POSTGRES_PORT = env.str("POSTGRES_PORT")
        self.POSTGRES_HOST = env.str("POSTGRES_HOST")
        self.DB_CONN_URL = f'postgresql+asyncpg://{env.str("POSTGRES_USER")}:{env.str("POSTGRES_PASSWORD")}@{env.str("POSTGRES_HOST")}:{env.str("POSTGRES_PORT")}/{env.str("POSTGRES_DB")}'


settings = Settings()
os.makedirs("logs", exist_ok=True)


answer = {
    'main': 'Привет выберите <b>"Каталоги"</b> или <b>"Поиск"</b>:',
    'about_us': 'Бот для удобной работы с онлайн магазинами',
    'cart': 'Корзина 🛒"',
    'catalogs': '<b>Cписок каталогов:</b>',
    'add_to_cart': 'Добавить в корзину'
}