from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from .forms import ReservationForm
from django.db.models import Q

def reservations_list(request):
    search = request.GET.get("search", "")
    reservations = Reservation.objects.all()

    if search:
        reservations = reservations.filter(
            Q(room__number__icontains=search) |
            Q(guest__last_name__icontains=search) |
            Q(guest__first_name__icontains=search)
        )
  
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

    return render(
        request,
        "reservations/reservation_form.html",
        {"form": form},
    ) 

def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == "POST":
        reservation.delete()
        return redirect("reservation_list")

    return render(
        request,
        "reservations/reservation_confirm_delete.html",
        {"reservation": Reservation},
    ) 