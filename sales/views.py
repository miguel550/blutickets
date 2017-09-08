from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, CreateView
from .models import Order, LineItem
from .forms import OrderSecondStepForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from tickets.models import Ticket


@login_required(login_url=reverse_lazy('account_login'))
def create_order(request, ticket_pk):

    if request.method == "GET":
        order, created = Order.objects.get_or_create(user=request.user,
                                                     status=Order.PREPARING)
        line_items = LineItem.objects.filter(order=order)
        if ticket_pk:
            ticket = get_object_or_404(Ticket, pk=ticket_pk)
            line_item, line_created = LineItem.objects.get_or_create(product=ticket,
                                                                     order=order,
                                                                     price=ticket.price)
            if not line_created:
                line_item.quantity += 1
                line_item.save()
        return render(request, 'sales/edit_order.html', {'order': order,
                                                         'line_items': line_items})


def edit_order_and_next(request):
    if request.method == "POST":
        # edit items quantity
        if 'order_id' in request.POST:
            order = get_object_or_404(Order, pk=request.POST['order_id'])
            form = OrderSecondStepForm(instance=order)
            return render(request, 'sales/edit_order_address.html', {
                'order': order,
                'form': form,
            })


def checkout(request):
    if request.method == "POST":
        # map location through post
        if 'order_id' in request.POST:
            order = get_object_or_404(Order, pk=request.POST['order_id'])
            # order.user = request.user
            form = OrderSecondStepForm(instance=order, data=request.POST)
            form = OrderSecondStepForm(instance=order, data=request.POST)
            if form.is_valid():
                form.save()
            order.status = Order.PENDING
            order.save()
            return render(request, 'sales/thank_you.html', {'order': order})


