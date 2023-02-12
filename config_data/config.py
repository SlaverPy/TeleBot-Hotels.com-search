"""Передает из файла .env токен бота"""

import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

logger.add('logs/logs.log', level='DEBUG', rotation='10:00')

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', 'Топ самых дешёвых отелей'),
    ('recommended', 'Рекомендуемые отели'),
    ('relevant', 'Наиболее релевантные по цене отели'),
    ('history', 'Узнать историю поиска отелей'),
    ('cancel', 'Отменить поиск'),
)


MISTAKE = """Возникли проблемы с сервером.
Запрос информации в данный момент не возможен.
Просим прощения за доставленные неудобства.
Попробуйте повторить запрос позже."""

MISTAKE_HOTEL = """Возникли проблемы с сервером.
Не получилось запросить детальную информацию об отеле.
Просим прощения за доставленные неудобства.
Попробуйте повторить запрос позже."""

URL_SEARCH = "https://hotels4.p.rapidapi.com/locations/v3/search"
URL_HOTEL_INFO = "https://hotels4.p.rapidapi.com/properties/v2/list"
URL_PHOTO = "https://hotels4.p.rapidapi.com/properties/v2/detail"

HEADERS_POST = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

HEADERS_GET = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
