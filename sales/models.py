from django.db import models
from django.contrib.auth.models import User
from tickets.models import Ticket
from geoposition.fields import GeopositionField


class LineItem(models.Model):
    product = models.ForeignKey(Ticket)
    order = models.ForeignKey('Order')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=8)


class Order(models.Model):
    PREPARING = 'preparing'
    PENDING = 'pending'
    REJECTED = 'rejected'
    APPROVED = 'approved'
    CLOSED = 'closed'
    STATUS_CHOICES = (
        (PREPARING, 'Preparación'),
        (PENDING, 'En espera'),
        (REJECTED, 'Rechazado'),
        (APPROVED, 'Aprovado'),
        (CLOSED, 'Cerrado'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PREPARING,
    )
    line_items = models.ManyToManyField(Ticket, through='LineItem')
    map_position = GeopositionField(null=True, blank=True)
    user = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden:{self.pk}"

