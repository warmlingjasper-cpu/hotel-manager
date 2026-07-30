from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "guest",
            "room",
            "check_in",
            "check_out",
            
        ]