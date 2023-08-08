from django.urls import include, path

urlpatterns = [
    path("api/", include("data_handler.urls")),
    path("api/", include("delivery.urls")),
]
