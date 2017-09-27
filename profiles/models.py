from django.db import models
from django.contrib.auth.models import AbstractUser


class Province(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey('Province')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Sector(models.Model):
    # Sectors are from wwww.codigopostalrepublicadominicana.com
    # Filtered with only unique sector's names
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    province = models.ForeignKey('Province', null=True)
    municipality = models.ForeignKey('Municipality', null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        # In case of District then province name will be used.
        if self.province:
            where = str(self.province)
        # Otherwise will use the municipality name.
        elif self.municipality:
            where = str(self.municipality)
        return f"{self.name}, {where}"

    class Meta:
        unique_together = ("code", "name")


class User(AbstractUser):
    # ISO 3166-2:DO standard codes for Dominican Republic
    # Reference: http://www.jmarcano.com/mipais/diversos/iso3166.html
    DISTRITO_NACIONAL = 1
    sector = models.ForeignKey('Sector', null=True)
    phone_number_primary_type = models.CharField(max_length=15, default="")
    phone_number_primary = models.CharField(max_length=15, default="")
    phone_number_secondary_type = models.CharField(max_length=15, default="")
    phone_number_secondary = models.CharField(max_length=15, default="")
