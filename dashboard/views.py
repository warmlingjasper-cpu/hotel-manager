from django.shortcuts import render
from rooms.models import Room
from guests.models import Guest
from reservations.models import Reservation


def index(request):

    context = {
        "rooms": Room.objects.count(),
        "guests": Guest.objects.count(),
        "reservations": Reservation.objects.count(),
    }

    return render(request, "dashboard/index.html", context)