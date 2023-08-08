from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .pochta_rf_utils import get_pochta_rf_data
from .serializers import OrderSerializer
from .sdek_utils import get_sdek_data


@api_view(["POST"])
def get_costs(request):
    """Получение данных."""
    serializer = OrderSerializer(
        data=request.data,
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = {
        "SDEK_DATA": get_sdek_data(serializer.data, settings.TARIFF_COUNT),
        "POCHTA_RF_DATA": get_pochta_rf_data(serializer.data),
    }
    return Response(data, status=status.HTTP_200_OK)
