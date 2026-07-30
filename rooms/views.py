from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from .forms import RoomForm
from django.db.models import Q

def room_list(request):
    search = request.GET.get("search", "")
    rooms = Room.objects.all()

    if search:
        rooms = rooms.filter(
            Q(number__icontains=search) |
            Q(room_type__icontains=search)
        )
  
    return render(
        request,
        "rooms/room_list.html",
        {
            "rooms": rooms
        }
    )


def room_create(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("room_list")

    else:
        form = RoomForm()

    return render(
        request,
        "rooms/room_form.html",
        {
            "form": form
        }
    )

def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect("room_list")

    else:
        form= RoomForm(instance=room)

    return render(
        request,
        "rooms/room_form.html",
        {
            "form": form
        }  
    )

def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        room.delete()
        return redirect("room_list")

    return render(
        request,
        "rooms/room_confirm_delete.html",
        {
            "room": room
        }
    )
    

                               