from django.db import models
from django.contrib.auth import get_user_model
from tickets.models import Ticket
from profiles.models import Sector
from geoposition.fields import GeopositionField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template import loader


class Address(models.Model):
    sector = models.ForeignKey(Sector)
    street_and_house = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)


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
        (PREPARING, 'Preparacion'),
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
    address = models.ForeignKey('Address', null=True)
    map_position = GeopositionField(null=True)
    user = models.ForeignKey(get_user_model(), null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden:{self.pk}"


@receiver(post_save, sender=Order, dispatch_uid="update_order_status")
def order_udpdated(sender, instance, created, raw, using, update_fields, **kwargs):
    c = {
        'user': instance.user,
    }
    if instance.status == Order.PENDING:
        email = EmailMultiAlternatives(
            "Orden de compra procesada!",
            loader.get_template(
                'email_templates/email_order_waiting_for_approval.html'
            ).render(c),
            to=[instance.user.email]
        )
        email.content_subtype = "html"
        email.send()
    elif instance.status == Order.APPROVED:
        email = EmailMultiAlternatives(
            "Orden de compra aprovada!",
            loader.get_template(
                'email_templates/email_order_approved.html'
            ).render(c),
            to=[instance.user.email]
        )
        email.content_subtype = "html"
        email.send()
    elif instance.status == Order.REJECTED:
        email = EmailMultiAlternatives(
            "Orden de compra rechazada.",
            loader.get_template(
                'email_templates/email_order_rejected.html'
            ).render(c),
            to=[instance.user.email]
        )
        email.content_subtype = "html"
        email.send()
