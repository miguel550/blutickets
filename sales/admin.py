from django.contrib import admin
from .models import Order, LineItem


class TermInlineAdmin(admin.TabularInline):
    model = Order.line_items.through


class OrderAdmin(admin.ModelAdmin):
    list_display = ('status', 'show_address', 'user', )
    fields = ('status',)

    inlines = (TermInlineAdmin,)

    def show_address(self, obj):
        if obj.address:
            return f"{obj.address.sector.name}, {obj.address.street_and_house}, {obj.address.reference}"
        return "No address."

admin.site.register(Order, OrderAdmin)
