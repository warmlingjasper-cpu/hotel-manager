from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from .forms import ReservationForm
from django.db.models import Q
from rooms.models import Room
from django.http import JsonResponse
from datetime import date, timedelta


def reservations_list(request):
    search = request.GET.get("search", "")
    reservations = Reservation.objects.all()

    if search:
        filters = (
            Q(room__number__icontains=search) |
            Q(guest__last_name__icontains=search) |
            Q(guest__first_name__icontains=search)
        )

        if search.isdigit():
            filters |= Q(id=int(search))

        reservations = reservations.filter(filters)

    return render(
        request,
        "reservations/reservation_list.html",
        {
            "reservations": reservations
        }
    )


def reservation_create(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reservation_list")

    else:
        form = ReservationForm()

    return render(
        request,
        "reservations/reservation_form.html",
        {
            "form": form
        }
    )

def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect("reservation_list")

    else:
        form = ReservationForm(instance=reservation)
        if reservation.room:
            form.fields["room"].queryset = Room.objects.filter(
                id=reservation.room.id
            )
        else:
            form.fields["room"].queryset = Room.objects.none()

    return render(
        request,
        "reservations/reservation_form.html",
        {
            "form": form,
            "reservation": reservation,
            "next": request.GET.get("next"),
            },
    ) 

def reservation_cancel(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == "POST":
        reservation.status = Reservation.Status.CANCELLED
        reservation.save()
        return redirect("reservation_list")

    return render(
        request,
        "reservations/reservation_confirm_cancel.html",
        {"reservation": reservation},
    ) 

def reservation_checkin(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if reservation.status != Reservation.Status.RESERVED:
        return redirect("reservation_list")

    reservation.status = Reservation.Status.CHECKIN
    reservation.save()

    reservation.room.status = Room.Status.OCCUPIED
    reservation.room.save()

    if request.GET.get("next") == "dashboard":
        return redirect("dashboard")

    return redirect("reservation_list")

def reservation_checkout(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if reservation.status != Reservation.Status.CHECKIN:
        return redirect("reservation_list")

    reservation.status = Reservation.Status.CHECKOUT
    reservation.save()

    reservation.room.status = Room.Status.DIRTY
    reservation.room.save()

    if request.GET.get("next") == "dashboard":
        return redirect("dashboard")

    return redirect("reservation_list")

def available_rooms(request):
    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")
    room_type = request.GET.get("room_type")
    reservation_id = request.GET.get("reservation_id")

    if not check_in or not check_out or not room_type:
        return JsonResponse([], safe=False)

    occupied = Reservation.objects.filter(
        check_in__lt=check_out,
        check_out__gt=check_in,
        room__isnull=False,
        status__in=[
            Reservation.Status.RESERVED,
            Reservation.Status.CHECKIN,
        ],
    )

    # Se estiver a editar uma reserva, ignora essa reserva
    if reservation_id:
        occupied = occupied.exclude(pk=reservation_id)

    occupied_rooms = occupied.values_list("room_id", flat=True)

    rooms = Room.objects.filter(
        room_type=room_type
    ).exclude(
        id__in=occupied_rooms
    )

    if reservation_id:
        reservation = Reservation.objects.get(pk=reservation_id)

        rooms = (rooms | Room.objects.filter(pk=reservation.room_id)).distinct()

    rooms = rooms.order_by("number")

    data = [
        {
            "id": room.id,
            "number": room.number,
            "status": room.status,
        }
        for room in rooms
    ]

    return JsonResponse(data, safe=False)

def availability(request):
    start = request.GET.get("start")
    end = request.GET.get("end")

    context = {}

    if start and end:

        start = date.fromisoformat(start)
        end = date.fromisoformat(end)

        days = []

        current = start

        while current <= end:
            days.append(current)
            current += timedelta(days=1)

        room_types = Room.objects.values_list(
            "room_type",
            flat=True
        ).distinct()

        availability = []

        for room_type in room_types:
            rooms = Room.objects.filter(
                room_type=room_type
                ).exclude(
                    status=Room.Status.BLOCKED
                )

            row ={
                "room_type": room_type,
                "counts": []
            }

            for day in days:
                occupied = Reservation.objects.filter(
                    status__in=[
                        Reservation.Status.RESERVED,
                        Reservation.Status.CHECKIN,
                    ],
                    check_in__lte=day,
                    check_out__gt=day,
                    room_type=room_type,
                ).count()

                available = rooms.count() - occupied
                row["counts"].append({
                    "value": available,
                    "warning": available <= 0,
                    })
            availability.append(row)

        context = {
            "days": days,
            "availability": availability,
            "start": start,
            "end": end,
        }

    return render(
        request,
        "reservations/availability.html",
        context
    )




