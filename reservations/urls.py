from django.urls import path
from . import views

urlpatterns = [
    path("", views.reservations_list, name="reservation_list"),
    path("new/", views.reservation_create, name="reservation_create"),
    path("update/<int:pk>/", views.reservation_update, name="reservation_update"),
    path("delete/<int:pk>/", views.reservation_delete, name="reservation_delete"),
]