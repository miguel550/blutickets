from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404, HttpResponse
from .models import Order, LineItem, Address
from .forms import OrderSecondStepForm, OrderSecondStepFormPhones
from django.contrib.auth.decorators import login_required
from django.views. decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from tickets.models import Ticket
from django.db import IntegrityError
from django.views.decorators.cache import never_cache
import re
import json
import requests
from django.db import transaction


@never_cache
@login_required(login_url=reverse_lazy('login-signup'))
def create_order(request):

    if request.method == "POST":
        order, created = Order.objects.get_or_create(user=request.user,
                                                     status=Order.PREPARING)
        if 'ticket_id' in request.POST:
            ticket = get_object_or_404(Ticket, pk=request.POST['ticket_id'])
            LineItem.objects.get_or_create(product=ticket,
                                           order=order,
                                           price=ticket.price)

        return redirect('create_order_or_add_item')
    elif request.method == "GET":
        recommended_events = Ticket.objects.filter(active=True)[:3]
        return render(request, 'sales/edit_order.html', {'recommended_events': recommended_events})


@never_cache
@login_required(login_url=reverse_lazy('login-signup'))
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
                                       map(pattern.match, request.POST.keys())))
            if order.lineitem_set.all().exists():
                items = []
                for line_item_id in line_item_ids:
                    items.append(get_object_or_404(LineItem, pk=line_item_id, order=order))
                try:
                    with transaction.atomic():
                        for item in items:
                            try:
                                quantity = int(request.POST[f'quantity_{item.pk}'])  # noqa: E901
                            except ValueError:
                                raise IntegrityError(f"'{request.POST[f'quantity_{item.pk}']}' is not a quantity.")

                            if item.product.remaining >= quantity > 0:
                                item.quantity = quantity
                            else:
                                raise IntegrityError(f"Trying to put {quantity} when remaining is {item.product.remaining}")  # noqa: E501
                            if item.product.ticket_types.all().exists():
                                try:
                                    type_id = int(request.POST[f'type_{item.pk}'])
                                except ValueError:
                                    raise IntegrityError(f"'{request.POST[f'type_{item.pk}']}' is not a number.")
                                item.ttype = get_object_or_404(item.product.ticket_types, id=type_id)
                                ticket_type = get_object_or_404(item.product.ticket_types.through,
                                                                ttype_id=type_id,
                                                                ticket=item.product)
                                item.price = ticket_type.price
                            item.save()

                except IntegrityError:
                    return redirect('create_order_or_add_item')

                # form_populated = OrderFirstStepForm(request.POST)
                # if form_populated.is_valid():
                #     form_populated.save()
                try:
                    last_order = request.user.order_set.exclude(
                                    status=Order.PREPARING
                                 ).latest()
                    address = last_order.address
                except Order.DoesNotExist:
                    # No last order found, this is the first order for the user
                    address = Address(sector=request.user.sector)

                form = OrderSecondStepForm(instance=address)
                form2 = OrderSecondStepFormPhones(instance=order.user)
                return render(request, 'sales/edit_order_address.html', {
                    'order': order,
                    'form': form,
                    'form_phones': form2,
                })
            return redirect('home')


@never_cache
@login_required(login_url=reverse_lazy('login-signup'))
def checkout(request):
    if request.method == "POST":
        # map location through post
        if 'order_id' in request.POST:
            order = get_object_or_404(Order, pk=request.POST['order_id'], user=request.user)
            # order.user = request.user
            form = OrderSecondStepForm(request.POST)
            form_phones = OrderSecondStepFormPhones(instance=request.user, data=request.POST)
            if form.is_valid() and form_phones.is_valid():
                form_phones.save()
                order.address = form.save()
                order.status = Order.PENDING
                order.save()
                return render(request, 'sales/thank_you.html', {'order': order})
            raise Http404("Transacción incompleta. Error: Datos inválidos.")


def remove_item_from_order(request):
    if request.method == "POST":
        if 'line_item_id' in request.POST:
            order = get_object_or_404(Order, user=request.user, status=Order.PREPARING)
            line_item = get_object_or_404(LineItem, pk=request.POST['line_item_id'], order=order)
            line_item.delete()
            return JsonResponse({'RESULT': 'OK'})


def send_slack_reponse(response, msg):
    response_url = response['response_url']
    payload = response['original_message']
    payload['attachments'][0].pop('actions')
    payload['attachments'][0].pop('callback_id')
    payload['attachments'][0]['fields'].append({
                        "title": "Status cambiado",
                        "value": msg,
                        "short": False
                    })
    requests.post(response_url, json=payload)


@csrf_exempt
def slack_actions(request):
    response = json.loads(request.POST['payload'])
    callback_id = response['callback_id']
    if callback_id == "change_order_status":
        if response['actions']:
            action = response['actions'][0]
            if action['name'] == "status":
                new_status, pk = action['value'].split()
                order = Order.objects.get(id=pk)
                if order.status != new_status:
                    order.status = new_status
                    order.save()
                if new_status == Order.APPROVED:
                    message = ":white_check_mark: Orden APROBADA"
                elif new_status == Order.REJECTED:
                    message = ":x: Orden RECHAZADA"
                message += f" por <@{response['user']['id']}|{response['user']['name']}>."
                send_slack_reponse(response,
                                   message)

                return HttpResponse("")
    return JsonResponse({'RESULT': 'No known action invoked'})
