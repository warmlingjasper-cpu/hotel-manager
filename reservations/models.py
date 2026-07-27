from django.db import models
from rooms.models import Room
from guests.models import Guest


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.guest} - Room {self.room.number}"