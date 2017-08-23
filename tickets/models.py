from django.db import models


class Ticket(models.Model):
    party_name = models.CharField(max_length=150)
    flyer_image = models.ImageField()
    direction = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.party_name
