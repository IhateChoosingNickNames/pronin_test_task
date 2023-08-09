import json

from rest_framework import status
from rest_framework.test import APITestCase


class DeliveryTests(APITestCase):
    __url = "/api/v1/check-delivery-cost/"
    __methods = ("POST",)

    def test_correct_data_real_requests(self):
        correct_data = "data_for_tests/delivery/correct_order_data.json"
        correct_response_data = (
            "data_for_tests/delivery/correct_order_response_data.json"
        )
        with open(correct_data, encoding="utf-8") as file:
            response = self.client.post(self.__url, data=json.load(file))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with open(correct_response_data, encoding="utf-8") as file:
            self.assertEqual(
                response.json(),
                json.load(file),
                "Ответ не совпадает с ожидаемым",
            )

    def test_incorrect_data_real_requests(self):
        correct_data = "data_for_tests/delivery/incorrect_order_data.json"

        with open(correct_data, encoding="utf-8") as file:
            response = self.client.post(self.__url, data=json.load(file))

        self.assertNotEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Проверьте, что при некоторетных данных райзится ошибка",
        )
