from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "room_type",
        "capacity",
        "price_per_night",
        "status",
    )

    list_filter = (
        "room_type",
        "status",
    )

    search_fields = (
        "number",
        "room_type",
    )

    ordering = ("number",)