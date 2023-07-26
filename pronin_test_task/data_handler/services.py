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
    # Корректный сырой запрос
    return ClientGem.objects.raw(
        'SELECT id, sum(costs) as spent_money FROM '
        '"data_handler_clientgem" GROUP BY client_id '
        'ORDER BY spent_money DESC LIMIT 5'
    )
