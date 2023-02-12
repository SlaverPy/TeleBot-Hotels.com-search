from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from config_data.config import URL_SEARCH
from functions.for_working_with_API.request_to_API import request_to_api_get


def city_founding(city) -> list:
    """Функция для поиска города
    принимает:
        city : 'Название города'

    формирует 'querystring'

    выполняет запрос к функции: 'request_to_api_get'
    формирует список из полученного запроса с именем и id городов
    Возвращает сформированный список
    """
    querystring = {"q": city, "locale": "ru_RU", "langid" : "1033", "siteid" : "300000001"}
    response = request_to_api_get(url=URL_SEARCH, querystring=querystring)
    result = response.json()
    cities = list()
    for x in result['sr']:
        if x['type'] == "CITY" or x['type'] == 'NEIGHBORHOOD' or x['type'] == 'MULTIREGION':
            cities.append({'city_name': x['regionNames']['fullName'], 'destination_id': x["gaiaId"]})
    return cities


def choosing_a_city(city) -> InlineKeyboardMarkup:
    """Функция для вывода кнопок
    Создает кнопки с названиями городов/регионов/областей

    принимает:
        city : 'Название города'

    передает название города в функцию: 'city_founding'
    выводит кнопки с :
        text= 'Название города',
        callback_data= f'id города'
    Возвращает кнопки в столбик
    """
    cities = city_founding(city)
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'],
                                              callback_data=f'{city["destination_id"]}',
                                              resize_keyboard=True))
    return destinations
