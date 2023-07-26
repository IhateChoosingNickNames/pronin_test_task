from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .exceptions import IncorrectFileError
from .serializers import DataSerializer
from .services import get_clients
from .utils import parse_csv_file


@cache_page(settings.CACHE_TIMEOUT)
@api_view(["GET"])
def get_data(request):
    """Получение данных."""
    clients = get_clients()
    serializer = DataSerializer(
        many=True,
        data=list(clients),
    )
    # TODO добавить обработку ошибок
    serializer.is_valid()
    return Response({"response": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_data(request):
    """Получение и обработка файла."""
    try:
        file = request.data["deals"]
        decoded_file = file.read().decode()
        parse_csv_file(decoded_file)
    except KeyError:
        return Response(
            {
                "status": "error",
                "Desc": "Файл нужно передавать по ключу deals",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    except AttributeError:
        return Response(
            {"status": "error", "Desc": "Файл не был передан"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except IncorrectFileError as e:
        return Response(
            {"status": "error", "Desc": e.args[0]},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"status": "error", "Desc": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    cache.clear()
    return Response({"status": "success"}, status=status.HTTP_200_OK)
