from django.conf import settings
from django.db.models import Sum

from .models import Client, ClientGem, Gem


def __get_objects(model, field, initial_data):
    """Создание всех недостающих пользователей."""
    result_data = initial_data.copy()
    filter_data = {f"{field}__in": initial_data.keys()}
    objs = model.objects.filter(**filter_data)

    for obj in objs:
        result_data[getattr(obj, field)] = obj

    bulks = [
        model(**{field: name})
        for name, db_obj in result_data.items()
        if db_obj is None
    ]

    for obj in model.objects.bulk_create(bulks):
        result_data[getattr(obj, field)] = obj

    return result_data


def save_data_to_db(data):
    """Сохранение записи в БД."""
    client_usernames, gem_names, deals = {}, {}, []

    for s in data:
        client_usernames[s["customer"]] = None
        gem_names[s["item"]] = None

    clients = __get_objects(Client, "username", client_usernames)
    gems = __get_objects(Gem, "name", gem_names)

    for new_deal in data:
        client = clients[new_deal["customer"]]
        gem = gems[new_deal["item"]]

        deals.append(
            ClientGem(
                client=client,
                gem=gem,
                quantity=new_deal["quantity"],
                costs=new_deal["total"],
                deal_date=new_deal["date"],
            )
        )

    ClientGem.objects.bulk_create(deals)


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
