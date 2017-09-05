from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .forms import ShowMapForm

from .models import Ticket


class TicketList(ListView):
    model = Ticket


class TicketDetailView(DetailView):
    model = Ticket

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ShowMapForm(instance=ctx['object'])
        return ctx


