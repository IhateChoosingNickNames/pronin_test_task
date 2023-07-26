import csv
import io

from django.conf import settings
from rest_framework.exceptions import ValidationError

from .services import save_data_to_db


def valid_data(data):
    """
    Проверка корректности входной строки в CSV.
    Если какое-то из полей неопределено - строка игнорируется.
    """

    for field in settings.DATA_FIELDS:
        if not data[field]:
            return False
    return True


def validate_headers(headers):
    if sorted(settings.DATA_FIELDS) != sorted(headers):
        raise ValidationError("Файл не соответствует нужному формату.")


def parse_csv_file(decoded_file):
    """Парсиннг CSV-файла в словарь."""
    io_string = io.StringIO(decoded_file)
    headers = list(
        map(str.strip, io_string.readline().split(settings.DELIMITER))
    )
    validate_headers(headers)
    parsed_data = csv.DictReader(io_string, fieldnames=headers)
    for new_deal in parsed_data:
        if valid_data(new_deal):
            save_data_to_db(new_deal)
