from rest_framework.exceptions import ValidationError


def _validate_keys(response, *keys):
    """Проверка наличия всех нужных ключей в ответе."""
    for key in keys:
        if key not in response:
            raise ValidationError(
                f"В ответе отсутствует ключ {key}"
                f"{response['errors']}"
            )


def _validate_instance(response, type_):
    """Проверка ответа на принадлежность к заданному типу данных."""
    if not isinstance(response, type_):
        raise ValidationError(
            f"Тип ответа {type(response)} не соответствует нужному {type_}"
        )
    if type_ == list and len(response) == 0:
        raise ValidationError(
            "Полученный список пуст, проверьте корректность входных данных"
        )
