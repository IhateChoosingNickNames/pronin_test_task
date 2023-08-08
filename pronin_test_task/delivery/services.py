import requests
from rest_framework.exceptions import ParseError, ValidationError


def _send_request(url, method, data, headers=None):
    _mapper = {
        "GET": requests.get,
        "POST": requests.post,
    }
    try:
        return _mapper[method](url, data, headers=headers).json()
    except requests.exceptions.ConnectionError:
        raise ParseError(f"Ошибка соединения с API {url}")
    except requests.exceptions.JSONDecodeError:
        raise ValidationError("API вернул не сериализуемый формат")
    except Exception as error:
        raise ParseError(f"Непредвиденная ошибка {type(error)} {error}")
