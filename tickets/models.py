from django.db import models


class Ticket(models.Model):
    party_name = models.CharField(max_length=150)
    flyer = models.ImageField(upload_to='media/flyers/')
    direction = models.CharField(max_length=250)
    description = models.TextField()

