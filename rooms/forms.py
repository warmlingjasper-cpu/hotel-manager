from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            "number",
            "room_type",
            "capacity",
            "price_per_night",
            "status",
        ]