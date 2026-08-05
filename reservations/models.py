from django.db import models
from rooms.models import Room
from guests.models import Guest


class Reservation(models.Model):

    class Status(models.TextChoices):
        RESERVED = "reserved", "Reserved"
        CHECKIN = "checkin", "check-in"
        CHECKOUT = "checkout", "check-out"
        CANCELLED = "cancelled", "Cancelled"

    room_type = models.CharField(
        max_length=20,
        choices=Room.RoomType.choices,
        blank=True,
        null=True
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )
    
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RESERVED
    )

    def __str__(self):
        return f"{self.guest} - Room {self.room}"
    

