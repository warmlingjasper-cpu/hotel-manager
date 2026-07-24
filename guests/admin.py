from django.contrib import admin

from .models import Guest

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "nationality",
        "date_of_birth",
        
    )

    list_filter = (
        "last_name",
    )

    search_fields = (
        "name",
        "last_name",
    )

    ordering = ("last_name", 
                "first_name",
                )