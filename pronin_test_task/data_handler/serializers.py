from rest_framework import serializers

from .models import Client, Gem


class GemsSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации о камне."""

    class Meta:
        model = Gem
        fields = ("name",)


class DataSerializer(serializers.ModelSerializer):
    """Сериалиазатор для вывода информации о пользователе."""

    spent_money = serializers.SerializerMethodField()
    gems = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ("username", "spent_money", "gems")

    @staticmethod
    def get_spent_money(obj):
        return obj.spent_money

    def get_gems(self, obj):
        client_ids = [
            client.id
            for client in self.initial_data
            if client.id != obj.id
        ]
        return GemsSerializer(obj.get_gems(client_ids), many=True).data
