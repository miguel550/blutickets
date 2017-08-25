from django.db import models


class Ticket(models.Model):
    party_name = models.CharField(max_length=150)
    flyer_image = models.ImageField()
    address = models.CharField(max_length=250)
    description = models.TextField()
    when = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.party_name
