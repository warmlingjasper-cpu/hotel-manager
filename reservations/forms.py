from django import forms
from .models import Reservation
from rooms.models import Room
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField

class RoomChoiceField(ModelChoiceField):
    def label_from_instance(self, room):

        if room.status == Room.Status.CLEAN:
            dot = "🔵"
        elif room.status == Room.Status.INSPECTED:
            dot = "🟢"
        elif room.status == Room.Status.DIRTY:
            dot = "🔴"
        elif room.status == Room.Status.OCCUPIED:
            dot = "🟠"
        elif room.status == Room.Status.BLOCKED:
            dot = "⚫"
        else:
            dot = "⚪"

        return f"{dot} Room {room.number}"

class ReservationForm(forms.ModelForm):

    room = RoomChoiceField(
        queryset=Room.objects.none(),
        required=False,
    )

    class Meta:
        model = Reservation
        fields = [
            "guest",
            "room_type",
            "room",
            "check_in",
            "check_out",
        ]

        widgets = {
            "check_in": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "check_out": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["check_in"].input_formats = ["%Y-%m-%d"]
        self.fields["check_out"].input_formats = ["%Y-%m-%d"]

        self.fields["room"].queryset = Room.objects.order_by("number")

    def clean(self):
        cleaned_data = super().clean()

        room = cleaned_data.get("room")
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if room and check_in and check_out:
            overlap = Reservation.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in,
                status__in=[
                    Reservation.Status.RESERVED,
                    Reservation.Status.CHECKIN,
                ],
            )

            if self.instance.pk:
                overlap = overlap.exclude(pk=self.instance.pk)

            if overlap.exists():
                raise ValidationError(
                    f"Room {room.number} is already reserved for the selected dates."
                )
        return cleaned_data

    

