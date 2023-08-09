import json

from django.conf import settings

from .services import _send_request
from .validators import _validate_instance, _validate_keys


def _get_city_code(postal_code, headers):
    """Получение кода города от базы СДЭК."""
    body = {
        "country_codes": settings.LANGUAGE_CODE.upper(),
        "postal_code": postal_code,
    }
    response = _send_request(
        url=settings.SDEK_CITIES_URL, method="GET", data=body, headers=headers
    )
    _validate_instance(response, list)
    _validate_keys(response[0], "code")
    return response[0]["code"]


def _get_client_token(user_data):
    """Регистрация клиента."""
    response = _send_request(
        url=settings.SDEK_USER_REGISTER_URL, method="POST", data=user_data
    )
    _validate_keys(response, "access_token")
    return response["access_token"]


def _get_headers(token):
    """Формирование хедеров."""
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }


def _get_body(data, sender_city_id, receiver_city_id):
    """Формирование тела запроса."""
    package = {
        "weight": data.get("weight"),
        "length": data.get("length"),
        "width": data.get("width"),
        "height": data.get("height"),
    }
    return {
        "currency": settings.SDEK_CURRENCY,
        "lang": settings.SDEK_LANG,
        "from_location": {"code": sender_city_id},
        "to_location": {"code": receiver_city_id},
        "packages": [package],
    }


def _get_result_response(data, limit):
    """Формирование результирующего ответа."""
    return [
        {"tariff": elem["tariff_name"], "price": elem["delivery_sum"]}
        for elem in data[:limit]
    ]


def get_sdek_data(data, limit):
    """Основная функция получения данных от СДЭК."""
    token = _get_client_token(settings.SDEK_TEST_USER_DATA)
    headers = _get_headers(token)
    sender_city_id = _get_city_code(
        data["sending_city_postal_code"], headers
    )
    receiver_city_id = _get_city_code(
        data["receiving_city_postal_code"], headers
    )
    body = _get_body(data, sender_city_id, receiver_city_id)
    response = _send_request(
        url=settings.SDEK_CALCULATOR_URL,
        data=json.dumps(body),
        method="POST",
        headers=headers,
    )
    _validate_keys(response, "tariff_codes")
    return _get_result_response(response["tariff_codes"], limit)
