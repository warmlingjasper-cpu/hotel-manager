from django.shortcuts import render, redirect, get_object_or_404
from .models import Guest
from .forms import GuestForm
from django.db.models import Q

def guest_list(request):
    search = request.GET.get("search", "")
    guests = Guest.objects.all().order_by("last_name", "first_name")

    if search:
        guests = guests.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(nationality__icontains=search)
        )
    return render(
        request,
        "guests/guest_list.html",
        {
            "guests": guests,
            "search": search,
        }
    )

def guest_create(request):
    if request.method == "POST":
        form = GuestForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("guest_list")

    else:
        form = GuestForm()

    return render(
        request,
        "guests/guest_form.html",
        {
            "form": form
        }
    )

def guest_delete(request, pk):
    guest = get_object_or_404(Guest, pk=pk)

    if request.method == "POST":
        guest.delete()
        return redirect("guest_list")

    return render(
        request,
        "guests/guest_confirm_delete.html",
        {"guest": Guest},
    ) 

def guest_update(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == "POST":
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return redirect("guest_list")

    else:
        form = GuestForm(instance=guest)

    return render(
        request,
        "guests/guest_form.html",
        {"form": form},
    ) 