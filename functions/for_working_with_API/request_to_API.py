from typing import Union
from requests import Response

import requests

from config_data.config import HEADERS_GET, HEADERS_POST, MISTAKE


def request_to_api_post(url: str, payload: dict) -> Union[Response, str]:
    """Функция для совершения post запросов к API
    Принимает 2 аргумента:
        url: str
        payload: dict
    Возвращает результат запроса или сообщение об ошибки
    """
    try:
        response = requests.request("POST", url=url, headers=HEADERS_POST, json=payload, timeout=10)
        if response.status_code == requests.codes.ok:
            return response
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as ex:
        return MISTAKE


def request_to_api_get(url: str, querystring: dict) -> Union[Response, str]:
    """Функция для совершения get запросов к API
    Принимает 2 аргумента:
        url: str
        querystring: dict
    Возвращает результат запроса или сообщение об ошибки
    """
    try:
        response = requests.request("GET", url, headers=HEADERS_GET, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as ex:
        return MISTAKE
