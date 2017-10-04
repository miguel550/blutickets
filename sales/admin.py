from django.contrib import admin
from . import models


class TermInlineAdmin(admin.TabularInline):
    model = models.Order.line_items.through


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        'show_address',
        'user',
        'user_number_primary',
        'user_number_secondary'
    )
    fields = ('status',)

    inlines = (TermInlineAdmin,)

    def show_address(self, obj):
        if obj.address:
            return f"{obj.address.sector.name}, {obj.address.street_and_house}, {obj.address.reference}"
        return "No address."

    def user_number_primary(self, obj):
        if obj.user.phone_number_primary:
            return obj.user.phone_number_primary
        return "No hay telefono."

    def user_number_secondary(self, obj):
        if obj.user.phone_number_secondary:
            return obj.user.phone_number_secondary
        return "No hay telefono."

