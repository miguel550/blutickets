from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Order, LineItem
from .forms import OrderSecondStepForm, OrderFirstStepForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from tickets.models import Ticket
import re


@login_required(login_url=reverse_lazy('account_login'))
def create_order(request):

    if request.method == "POST":
        order, created = Order.objects.get_or_create(user=request.user,
                                                     status=Order.PREPARING)
        line_items = LineItem.objects.filter(order=order)
        if 'ticket_id' in request.POST:
            ticket = get_object_or_404(Ticket, pk=request.POST['ticket_id'])
            line_item, line_created = LineItem.objects.get_or_create(product=ticket,
                                                                     order=order,
                                                                     price=ticket.price)

        return redirect('create_order_or_add_item')
    elif request.method == "GET":
        try:
            order = Order.objects.get(user=request.user,
                                      status=Order.PREPARING)
        except Order.DoesNotExist:
            order = None
        line_items = None
        if order:
            line_items = LineItem.objects.filter(order=order)

        return render(request, 'sales/edit_order.html', {'order': order,
                                                         'line_items': line_items})


def edit_order_and_next(request):
    if request.method == "POST":
        # edit items quantity

        if 'order_id' in request.POST:
            order = get_object_or_404(Order,
                                      pk=request.POST['order_id'],
                                      user=request.user,
                                      status=Order.PREPARING)
            pattern = re.compile(r"^quantity_(?P<line_item_id>\d+)$")
            line_item_ids = map(lambda x: x.group('line_item_id'),
                                filter(None,
                                       map(pattern.match,  request.POST.keys())))
            items = []
            for line_item_id in line_item_ids:
                items.append(get_object_or_404(LineItem, pk=line_item_id, order=order))
            for item in items:
                try:
                    quantity = int(request.POST[f'quantity_{item.pk}'])
                except:
                    quantity = 0
                if item.product.remaining >= quantity > 0:
                    item.quantity = quantity
                    item.save()

            # form_populated = OrderFirstStepForm(request.POST)
            # if form_populated.is_valid():
            #     form_populated.save()

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
            if form.is_valid():
                form.save()
            order.status = Order.PENDING
            order.save()
            return render(request, 'sales/thank_you.html', {'order': order})


def remove_item_from_order(request):
    if request.method == "POST":
        if 'line_item_id' in request.POST:
            order = get_object_or_404(Order, user=request.user, status=Order.PREPARING)
            line_item = get_object_or_404(LineItem, pk=request.POST['line_item_id'], order=order)
            line_item.delete()
            return JsonResponse({'RESULT': 'OK'})



