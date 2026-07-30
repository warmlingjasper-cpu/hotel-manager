from django.shortcuts import render
from rooms.models import Room
from guests.models import Guest
from reservations.models import Reservation
from datetime import date, timedelta

def index(request):

    selected_date = request.GET.get("date")
    
    if selected_date:
        selected_date = date.fromisoformat(selected_date)
    else:
        selected_date = date.today()

    checkins = Reservation.objects.filter(
        check_in=selected_date
    ).order_by("room__number")

    inhouse = Reservation.objects.filter(
        check_in__lte=selected_date,
        check_out__gt=selected_date
    ).order_by("room__number")

    checkouts = Reservation.objects.filter(
        check_out=selected_date
    ).order_by("room__number")

    total_rooms = Room.objects.count()

    available_rooms = total_rooms - inhouse.count()

    occupancy = 0
    if total_rooms > 0:
        occupancy = round((inhouse.count()/total_rooms) *100)

    context = {
        "selected_date": selected_date.strftime("%Y-%m-%d"),
        "selected_date_long": selected_date.strftime("%A, %d %B %Y"),

        "previous_date": (selected_date - timedelta(days=1)).strftime("%Y-%m-%d"),
        "next_date": (selected_date + timedelta(days=1)).strftime("%Y-%m-%d"),

        "checkins": checkins,
        "inhouse": inhouse,
        "checkouts": checkouts,

        "rooms": Room.objects.count(),
        "available_rooms": available_rooms,
        "inhouse_count": inhouse.count(),
        "checkins_count": checkins.count(),
        "checkouts_count": checkouts.count(),
        "occupancy": occupancy,

        "guests": Guest.objects.count(),
        "reservations": Reservation.objects.count(),
    }

    return render(request, "dashboard/index.html", context)

