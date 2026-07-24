from django.db import models

class Reservations(models.Model):
    Room_number = models.CharField(max_length=50)
    Guest = models.CharField(max_length=50)
    Check_in_date = models.DateField()
    Check_out_date = models.DateField()

    def __str__(self):
        return f"{Guest} {Room_number} {Check_in_date} {Check_out_date}"