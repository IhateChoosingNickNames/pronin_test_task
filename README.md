# pronin_test_task
Test task for Pronin


### Project description:

Web application for recieving, parsing data in CSV-format.

Used technologies:
-
    - python 3.11
    - django 4.2
    - djangorestframework 3.14
    - python-dotenv 0.21.1
    - PostgreSQL 13.0
    - Docker 20.10.22
    - Poetry 1.4.0

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

### Project author:

Larkin Mikhail
https://github.com/IhateChoosingNickNames