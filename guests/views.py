from django.shortcuts import render, redirect, get_object_or_404
from .models import Guest
from .forms import GuestForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages

def guest_list(request):
    search = request.GET.get("search", "")
    guests = Guest.objects.all().order_by("last_name", "first_name")

    if search:
        filters = (
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(nationality__icontains=search)
        )

        if search.isdigit():
            filters |= Q(id=int(search))
        
        guests = guests.filter(filters)

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
            messages.success(request, "Guest created successfully!")
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
        messages.success(request, "Guest deleted successfully!")
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
            messages.success(request, "Guest updated successfully!")
            return redirect("guest_list")

    else:
        form = GuestForm(instance=guest)

    return render(
        request,
        "guests/guest_form.html",
        {
            "form": form,
            "guest": guest,
            },
    ) 

def guest_create_ajax(request):
    if request.method == "POST":
        form = GuestForm(request.POST)

        if form.is_valid():
            guest = form.save()

            return JsonResponse({
                "success": True,
                "id": guest.id,
                "name": f"{guest.first_name} {guest.last_name}",
            })
        return JsonResponse({
                "success": False,
                "errors": form.errors,
        })

    
    form = GuestForm()

    return render(
        request,
        "guests/guest_form_modal.html",
        {
            "form": form
        },
    ]