from django.db import models

class Room(models.Model):
    class Status(models.TextChoices):
        CLEAN = "CL", "Clean"
        DIRTY = "DI", "Dirty"
        INSPECTED = "IN", "Inspected"
        BLOCKED = "BL", "Blocked"

    number = models.IntegerField(unique=True)
    room_type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(
        max_digits=8, 
        decimal_places=2
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.CLEAN
        )
    
    def __str__(self):
        return f"Room {self.number}"


