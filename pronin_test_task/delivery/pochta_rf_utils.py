from django.conf import settings

from .services import _send_request
from .validators import _validate_keys


def _get_body(data, sender_city_post_id, receiver_city_post_id):
    """Формирование тела запроса."""
    return {
        "from": sender_city_post_id,
        "to": receiver_city_post_id,
        "weight": data["weight"],
        "length": data.get("length"),
        "width": data.get("width"),
        "height": data.get("height"),
    }


def get_pochta_rf_data(data):
    """Основная функция получения данных от Почты РФ."""
    sending_city_postal_code = data["sending_city_postal_code"]
    receiving_city_postal_code = data["receiving_city_postal_code"]
    body = _get_body(
        data, sending_city_postal_code, receiving_city_postal_code
    )
    response = _send_request(
        url=settings.POCHTA_RF_CALCULATOR_URL,
        data=body,
        method="GET",
        headers={"Content-Type": "application/json"},
    )
    _validate_keys(response, "name", "paymoneynds")
    return {
        "tariff": response["name"],
        "price": response["paymoneynds"] / settings.MONEY_KOEF,
    }
