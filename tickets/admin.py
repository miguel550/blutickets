from django.contrib import admin

from . import models


class TicketTypeInline(admin.TabularInline):
    model = models.Ticket.ticket_types.through


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = (TicketTypeInline,)


admin.site.register(models.Type)
