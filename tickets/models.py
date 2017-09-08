from django.db import models
from geoposition.fields import GeopositionField


class Ticket(models.Model):
    party_name = models.CharField(max_length=150)
    flyer_image = models.ImageField(upload_to='flyers')
    description = models.TextField()
    map_position = GeopositionField()
    when = models.DateTimeField()
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.party_name
