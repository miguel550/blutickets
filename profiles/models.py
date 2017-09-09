from django.db import models
from django.contrib.auth.models import AbstractUser


class Province(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Sector(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey('Province')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    # ISO 3166-2:DO standard codes for Dominican Republic
    # Reference: http://www.jmarcano.com/mipais/diversos/iso3166.html
    DISTRITO_NACIONAL = 1
    sector = models.ForeignKey('Sector', null=True)
    phone_number_primary_type = models.CharField(max_length=15, default="")
    phone_number_primary = models.CharField(max_length=15, default="")
    phone_number_secondary_type = models.CharField(max_length=15, default="")
    phone_number_secondary = models.CharField(max_length=15, default="")
