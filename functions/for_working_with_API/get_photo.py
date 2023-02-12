import json
from typing import Union

from functions.for_working_with_API.request_to_API import request_to_api_post
from config_data.config import URL_PHOTO


def get_photo(id: int) -> Union[dict, str]:
    """Функция для получения фото отеля
    Принимает информацию об отеле,
    формирует querystring с id отеля
    Производит запрос и получает из него url и приставку для формирования ссылки на фото
    Возвращает сформированную ссылку на первое фото"""
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": id
    }
    response = request_to_api_post(url=URL_PHOTO, payload=payload)
    if isinstance(response, str):
        return response
    result = json.loads(response.text)
    return result
