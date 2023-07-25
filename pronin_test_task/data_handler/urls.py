from django.urls import path

from . import views

APP_NAME = "data_handler"

urlpatterns = [
    path("v1/add-data/", views.add_data),
    path("v1/get-data/", views.get_data),
]
