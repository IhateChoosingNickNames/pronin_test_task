# pronin_test_task
Test task for Pronin


### Project description:

Web application for recieving, parsing data in CSV-format, and calculating delivery costs.

Used technologies:
-
    - python 3.11
    - django 4.2
    - djangorestframework 3.14
    - python-dotenv 0.21.1
    - PostgreSQL 13.0
    - Docker 20.10.22
    - Poetry 1.4.0
    - Requests 2.31.0

# Launch instructions:


## Set enviroment:
Fill go to /infra folder and create and fill .env file according to shown in .env.sample file.
- SECRET_KEY=... # secret key from Django project
- DB_ENGINE=... # indicate that we are working with postgresql
- DB_NAME=... # database name
- POSTGRES_USER=... # login to connect to the database
- POSTGRES_PASSWORD=... # password to connect to the database (set your own)
- DB_HOST=db # name of the service (container)
- DB_PORT=5432 # port to connect to the database
- LOCALHOST=localhost
- LOCALHOST_IP=127.0.0.1
- CONTAINER_NAME=backend # name of your backend container


## Install docker compose and run:
    docker-compose up -d --build
For now app is available at localhost


If you'll need any *manage.py* commands then you'll want to use prefix:

    docker-compose exec backend python manage.py *comand*


Examples requests:
-
    - GET your_url/api/v1/get-data/

    - POST your_url/api/v1/add-data/
```json
{
  "deals": some_file.csv
}
```
    - POST your_url/api/v1/check-delivery-cost/
```json
{
    "sending_city_postal_code": 117209,
    "receiving_city_postal_code": 630000,
    "weight": 17000
}
```

Examples of responses:
-
    - GET {
        "response": [
                {
                    "username": "resplendent",
                    "spent_money": 14750,
                    "gems": [
                        {
                            "name": "Сапфир"
                        },
                        {
                            "name": "Цаворит"
                        }
                    ]
                },
            ]
        }

    - POST {"status": "success"}

    - POST {
    "status": "error",
    "Desc": "[ErrorDetail(string='Файл не соответствует нужному формату.', code='invalid')]"
    }

    - POST {
    "SDEK_DATA": [
        {
            "tariff": "Экспресс дверь-дверь",
            "price": 4060.0
        },
        {
            "tariff": "Экспресс дверь-склад",
            "price": 3900.0
        },
    ],
    "POCHTA_RF_DATA": {
        "tariff": "Посылка",
        "price": 2259.78
        }
    }

### Project author:

Larkin Mikhail
https://github.com/IhateChoosingNickNames