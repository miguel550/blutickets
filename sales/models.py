from django.db import models
from django.contrib.auth import get_user_model
from geoposition.fields import GeopositionField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings
import requests
from django.db.models import Sum, F, FloatField


class Address(models.Model):
    sector = models.ForeignKey('profiles.Sector')
    street_and_house = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)


class LineItem(models.Model):
    product = models.ForeignKey('tickets.Ticket')
    order = models.ForeignKey('Order')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=8)

    def total(self):
        return self.quantity*self.price


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
    line_items = models.ManyToManyField('tickets.Ticket', through='LineItem')
    address = models.ForeignKey('Address', null=True)
    map_position = GeopositionField(null=True)
    user = models.ForeignKey(get_user_model(), null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        order_total = self.lineitem_set.aggregate(total=Sum(F('quantity')*F('price'), output_field=FloatField()))
        return order_total['total']

    def __str__(self):
        return f"Orden:{self.pk}"


def send_sales_slack_notification(order):
    sales_webhook = settings.SALES_SLACK_CHANNEL
    requests.post(sales_webhook, json={

        "username": "SalesBot",
        "icon_emoji": ":moneybag:",
        "attachments": [
            {
                "fallback": f"Orden #{order.pk} en espera de confirmación",
                "pretext": f"Orden #{order.pk} en espera de confirmación",
                "color": "#82FA58",
                "fields": [
                    {
                        "title": "Usuario",
                        "value": f"{order.user.first_name} {order.user.last_name}\n"
                                 f"Teléfono({order.user.phone_number_primary_type}): {order.user.phone_number_primary}\n"
                                 f"Teléfono opcional({order.user.phone_number_secondary_type}): {order.user.phone_number_secondary}",
                        "short": False
                    },
                    {
                        "title": "Dirección",
                        "value": f"{order.address.sector.name}\nCalle: {order.address.street_and_house}\nReferencias: {order.address.reference}",
                        "short": False
                    },
                    {
                        "title": "Productos",
                        "value": "\n".join([f"Pidio {line_item.quantity} boleta(s) de '{line_item.product.party_name}' | RD${line_item.total()}"
                                            for line_item in order.lineitem_set.all()])+
                                 f"\nTotal: RD${order.total()}",
                        "short": False
                    },
                ],
                "callback_id": "change_order_status",
                "actions": [
                    {
                        "name": "status",
                        "text": "Aprobado",
                        "style": "primary",
                        "type": "button",
                        "value": f"{Order.APPROVED} {order.pk}",
                        "confirm": {
                            "title": "¿Estás seguro?",
                            "text": "Estás a punto de cambiar la orden a APROBADO.",
                            "ok_text": "Sí",
                            "dismiss_text": "No"
                        }
                    },
                    {
                        "name": "status",
                        "text": "Rechazado",
                        "style": "danger",
                        "type": "button",
                        "value": f"{Order.REJECTED} {order.pk}",
                        "confirm": {
                            "title": "¿Estás seguro?",
                            "text": "Estás a punto de cambiar la orden a RECHAZADO.",
                            "ok_text": "Sí",
                            "dismiss_text": "No"
                        }
                    }
                ]
            }
        ]
    })


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
        send_sales_slack_notification(order=instance)
    elif instance.status == Order.APPROVED:
        email = EmailMultiAlternatives(
            "Orden de compra aprobada!",
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
