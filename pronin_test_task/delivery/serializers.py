from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    """Сериализатор заказа."""

    sending_city_postal_code = serializers.IntegerField(
        help_text="Введите почтовый индекс отправителя", required=True
    )
    receiving_city_postal_code = serializers.IntegerField(
        help_text="Введите почтовый индекс получателя", required=True
    )
    weight = serializers.IntegerField(help_text="Введите массу", required=True)
    length = serializers.IntegerField(
        help_text="Введите длину", required=False
    )
    width = serializers.IntegerField(
        help_text="Введите ширину", required=False
    )
    height = serializers.IntegerField(
        help_text="Введите высоту", required=False
    )

    class Meta:
        fields = (
            "sending_city",
            "weight",
            "length",
            "width",
            "height",
        )
