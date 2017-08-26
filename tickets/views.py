from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Ticket


class TicketList(ListView):
    model = Ticket


class TicketDetailView(DetailView):
    model = Ticket



