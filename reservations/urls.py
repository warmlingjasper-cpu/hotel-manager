from django.urls import path
from . import views

urlpatterns = [
    path("", views.reservations_list, name="reservation_list"),
    path("new/", views.reservation_create, name="reservation_create"),
    path("update/<int:pk>/", views.reservation_update, name="reservation_update"),
    path("cancel/<int:pk>/", views.reservation_cancel, name="reservation_cancel"),
    path("checkin/<int:pk>/", views.reservation_checkin, name="reservation_checkin"),
    path("checkout/<int:pk>/", views.reservation_checkout, name="reservation_checkout"),
    path("available-rooms/", views.available_rooms, name="available_rooms_json"),
    path("availability/", views.availability, name="availability"),
]