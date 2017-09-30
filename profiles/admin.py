from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Sector)
admin.site.register(models.Municipality)
admin.site.register(models.Province)
