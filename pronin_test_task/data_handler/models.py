from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """Модель покупателя."""

    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Имя покупателя"),
    )
    gems = models.ManyToManyField(
        "Gem",
        verbose_name=_("Камни"),
        related_name="clients",
        through="ClientGem",
    )

    def __str__(self):
        return self.username[:30]


class Gem(models.Model):
    """Модель камней."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Название камня"),
    )

    def __str__(self):
        return self.name[:30]


class ClientGem(models.Model):
    """Промежуточная таблица для М:М покупателей и камней."""

    client = models.ForeignKey(
        Client,
        verbose_name=_("Покупатель"),
        on_delete=models.CASCADE,
        related_name="client_gem",
    )
    gem = models.ForeignKey(
        Gem,
        verbose_name=_("Камень"),
        on_delete=models.CASCADE,
        related_name="gem_client",
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Количество камней в сделке")
    )
    costs = models.PositiveBigIntegerField(verbose_name=_("Цена сделки"))
    deal_date = models.DateTimeField(
        verbose_name=_("Дата сделки"),
        db_index=True,
    )

    def get_gems(self, client_ids):
        """Фильтрация камней текущего пользователя по их наличию у других."""
        gems_ids = [
            elem.gem_id
            for elem in ClientGem.objects.filter(client_id__in=client_ids)
        ]
        return self.client.gems.filter(id__in=gems_ids).distinct()
