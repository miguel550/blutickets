from django.db import models
from geoposition.fields import GeopositionField
from markupfield.fields import MarkupField
from imagekit.models import ImageSpecField
from sales.models import Order
from django.db.models import Sum
import random
import string


def random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=25))


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TicketType(models.Model):
    ttype = models.ForeignKey('Type')
    ticket = models.ForeignKey('Ticket')
    price = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    quantity = models.IntegerField(default=0)


class Ticket(models.Model):
    party_name = models.CharField(max_length=150)
    flyer_image = models.ImageField(upload_to='flyers')
    flyer_image_compressed = ImageSpecField(source='flyer_image',
                                            format='JPEG',
                                            options={
                                                'quality': 70
                                            },)
    description = MarkupField(default_markup_type='markdown')
    map_position = GeopositionField()
    when = models.DateTimeField()
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=8, default=0)

    ticket_types = models.ManyToManyField('Type', through='TicketType')
    active = models.BooleanField(default=True)

    slug = models.SlugField(max_length=50, default=random_string, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def sold(self):
        sold_items = self.lineitem_set.exclude(
            order__status__in=[Order.PREPARING, Order.REJECTED]
        ).aggregate(Sum('quantity'))
        sum_items = sold_items['quantity__sum']
        if sum_items:
            return sum_items
        return 0

    @property
    def remaining(self):
        return self.quantity - self.sold

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('ticket-detail', args=[self.slug])

    def __str__(self):
        return self.party_name
