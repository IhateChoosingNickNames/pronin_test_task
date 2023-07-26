from django.conf import settings
from django.db.models import Sum

from .models import Client, ClientGem, Gem


def save_data_to_db(data):
    """Сохранение записи в БД."""
    client, _ = Client.objects.get_or_create(username=data["customer"])
    gem, _ = Gem.objects.get_or_create(name=data["item"])
    ClientGem.objects.create(
        client=client,
        gem=gem,
        quantity=data["quantity"],
        costs=data["total"],
        deal_date=data["date"],
    )


def get_clients():
    """Получение требуемых клиентов."""
    # Корректный сырой запрос
    # return ClientGem.objects.raw(
    #     'SELECT "data_handler_clientgem".id, sum(costs) as spent_money '
    #     'FROM "data_handler_clientgem" '
    #     'JOIN "data_handler_client" '
    #     'ON "data_handler_client".id = "data_handler_clientgem".client_id '
    #     'GROUP BY client_id '
    #     'ORDER BY spent_money DESC '
    #     'LIMIT 5'
    # )

    clientgems = (
        ClientGem.objects.values("client_id")
        .annotate(spent_money=Sum("costs"))
        .order_by("-spent_money")[: settings.CLIENT_LIMIT]
        # .filter(deal_date__gt=)  # Если нужна будет фильтрация по времени
    )
    result = []
    for elem in clientgems:
        client = Client.objects.get(id=elem["client_id"])
        client.spent_money = elem["spent_money"]
        result.append(client)
    return result
