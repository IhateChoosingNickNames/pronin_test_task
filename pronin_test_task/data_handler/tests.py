from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from data_handler.models import Client, ClientGem


class AccountTests(APITestCase):
    __ENDPOINTS = {
        "get-data": {
            "url": "/api/v1/get-data/",
            "allowed_methods": ("GET",),
        },
        "add-data": {
            "url": "/api/v1/add-data/",
            "allowed_methods": ("POST",),
        },
    }

    def __prepare_data(self):
        correct_csv = "data_for_tests/data_handler/correct_data.csv"
        post_url = self.__ENDPOINTS["add-data"]["url"]
        with open(correct_csv, encoding="utf-8") as file:
            response = self.client.post(post_url, data={"deals": file})
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Проверьте корректность обработки CSV файлов.",
        )

    def test_urls_allowed_methods(self):
        __methods = (
            (self.client.get, "GET"),
            (self.client.post, "POST"),
            (self.client.put, "PUT"),
            (self.client.patch, "PATCH"),
            (self.client.delete, "DELETE"),
        )
        for endpoint in self.__ENDPOINTS:
            for method, method_name in __methods:
                response = method(self.__ENDPOINTS[endpoint]["url"])
                if (
                    method_name
                    not in self.__ENDPOINTS[endpoint]["allowed_methods"]
                ):
                    self.assertEqual(
                        response.status_code,
                        status.HTTP_405_METHOD_NOT_ALLOWED,
                    )

    def test_no_csv_file(self):
        url = self.__ENDPOINTS["add-data"]["url"]
        cases = ({}, {"deals": ""}, {"deals": ""})
        for data in cases:
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("status", response.data)
            self.assertEqual(response.data["status"], "error")

    def test_correct_csv_file(self):
        client_count_prev = Client.objects.count()
        self.assertEqual(client_count_prev, 0)

        self.__prepare_data()

        self.assertNotEqual(
            client_count_prev,
            Client.objects.count(),
            "Пользователи не были созданы",
        )

    def test_csv_with_wrong_headers(self):
        url = self.__ENDPOINTS["add-data"]["url"]
        wrong_headers_csv = "data_for_tests/data_handler/wrong_headers.csv"
        client_count_prev = Client.objects.count()
        self.assertEqual(client_count_prev, 0)

        with open(wrong_headers_csv, encoding="utf-8") as file:
            response = self.client.post(url, data={"deals": file})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "status", response.data, "В ответе должно быть поле status"
        )
        self.assertEqual(
            response.data["status"],
            "error",
            "В поле status должно быть значение error",
        )

        self.assertEqual(
            client_count_prev,
            Client.objects.count(),
            (
                "При несоответствующем формате файла не должно проиходить "
                "сохранений в БД"
            ),
        )

    def test_csv_with_wrong_body(self):
        url = self.__ENDPOINTS["add-data"]["url"]
        wrong_body_csv = "data_for_tests/data_handler/wrong_body.csv"
        client_count_prev = Client.objects.count()
        self.assertEqual(client_count_prev, 0)
        target_increment = 1

        with open(wrong_body_csv, encoding="utf-8") as file:
            response = self.client.post(url, data={"deals": file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            client_count_prev + target_increment,
            Client.objects.count(),
            (
                "Невалидные строки во входном файле не должны сохраняться в "
                "БД, а валидные - должны."
            ),
        )

    def test_correct_output(self):
        get_url = self.__ENDPOINTS["get-data"]["url"]

        target_data = [
            ("resplendent", 8502),
            ("bellwether", 5253),
            ("concoction", 2635),
            ("nambypamby", 1185),
            ("buckaroo", 342),
        ]
        self.__prepare_data()

        response = self.client.get(get_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "response", response.data, "Поле response должно быть в ответе"
        )
        self.assertEqual(
            len(response.data["response"]),
            settings.CLIENT_LIMIT,
            f"Проверьте, что в выдаче {settings.CLIENT_LIMIT} элементов",
        )

        first_element = response.data["response"][0]
        self.assertIn("username", first_element)
        self.assertIn("spent_money", first_element)
        self.assertIn("gems", first_element)

        response_data = [
            (elem["username"], int(elem["spent_money"]))
            for elem in response.data["response"]
        ]

        self.assertEqual(
            target_data,
            response_data,
            "Проверьте, что вы корректно возвращаете пользвоателей",
        )

    def test_cache(self):
        self.__prepare_data()

        get_url = self.__ENDPOINTS["get-data"]["url"]
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("response", response.data)
        self.assertEqual(len(response.data["response"]), settings.CLIENT_LIMIT)

        first_element = response.data["response"][0]
        previous_spent_money = first_element["spent_money"]
        client_id = Client.objects.get(username=first_element["username"]).id
        ClientGem.objects.filter(client_id=client_id).update(costs=0)

        response = self.client.get(get_url)

        current_first_element = response.data["response"][0]
        current_spent_money = current_first_element["spent_money"]

        self.assertEqual(first_element, current_first_element)
        self.assertEqual(
            previous_spent_money,
            current_spent_money,
            "Проверьте, что у вас корректно отрабатывает кэш",
        )

        cache.clear()

        response = self.client.get(get_url)

        current_first_element = response.data["response"][0]
        current_spent_money = current_first_element["spent_money"]

        self.assertNotEqual(
            first_element,
            current_first_element,
            "Проверьте, что при обновлении данных вы чистите кэш",
        )
        self.assertNotEqual(
            previous_spent_money,
            current_spent_money,
            "Проверьте, что при обновлении данных вы чистите кэш",
        )
