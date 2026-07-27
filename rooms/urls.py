from django.urls import path
from . import views

urlpatterns = [
    path("", views.room_list, name="room_list"),
    path("new/", views.room_create, name="room_create"),
    path("<int:pk>/edit/", views.room_update, name='room_update'),
    path("<int:pk>/delete/", views.room_delete, name='room_delete'),
]