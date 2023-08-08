from django.urls import path

from . import views

APP_NAME = "delivery"

urlpatterns = [
    path("v1/check-delivery-cost/", views.get_costs),
]
