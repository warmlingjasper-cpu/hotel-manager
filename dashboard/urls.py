from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("diagnostics/", views.reservation_diagnostics, name="reservation_diagnostics"),
]