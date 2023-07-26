from rest_framework.exceptions import ValidationError


class IncorrectFileError(ValidationError):
    pass
