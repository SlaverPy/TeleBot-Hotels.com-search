from functions.for_working_with_API.request_to_API import request_to_api_post
from config_data.config import URL_HOTEL_INFO

from typing import Union


def forming_querystring(data: dict) -> Union[dict, str]:
    """Функция для получения информации об отелях
    Принимает сформированный результат запроса от пользователя
    формирует querystring с внесенной пользователем информацией
    Производит запрос
    Возвращает результат полученный результат в формате json"""
    sort_order = ''
    filters = {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
    if data['command'] == '/lowprice':
        sort_order = 'PRICE_LOW_TO_HIGH'
    elif data['command'] == '/recommended':
        sort_order = 'RECOMMENDED'
    elif data['command'] == '/relevant':
        sort_order = "PRICE_RELEVANT"
        filters = {"price": {"max": int(data['price_max']), "min":  int(data['price_min'])}}
    payload = {
        "currency": 'USD',
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": data['city']},
        "checkInDate":
            {"day": data['date_of_entry'].day,
             "month": data['date_of_entry'].month,
             "year": data['date_of_entry'].year},
        "checkOutDate":
            {"day": data['date_of_departure'].day,
             "month": data['date_of_departure'].month,
             "year": data['date_of_departure'].year},
        "rooms": [{"adults": 1, "children": []}],
        "resultsStartingIndex": 0,
        "resultsSize": int(data['quantity']),
        "sort": sort_order,
        "filters": filters}
    response = request_to_api_post(url=URL_HOTEL_INFO, payload=payload)
    if isinstance(response, str):
        return response
    result = response.json()
    return result