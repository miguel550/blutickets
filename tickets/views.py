from django.shortcuts import render
from django.views.generic import ListView

from .models import Ticket


class TicketList(ListView):
    model = Ticket


def who_we_are(request):
    return render(request, 'who-we-are.html')


