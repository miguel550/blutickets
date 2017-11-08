from django.conf import settings
from sales.models import Order


def ga_tracking_id(request):
    return {
        'ga_tracking_id': settings.GA_TRACKING_ID,
        'ga_tracking_logged_in_id': settings.GA_TRACKING_LOGGED_IN_ID,
        'ga_tracking_anonymous_users_id': settings.GA_TRACKING_ANONYMOUS_USERS_ID,
    }


def use_ga(request):
    return {'use_ga': settings.USE_GA}


def cart(request):
    try:
        order_preparing = request.user.order_set.filter(status=Order.PREPARING).get()
        if order_preparing.line_items.count() <= 0:
            order_preparing = None
        return {'cart': order_preparing}
    except Order.DoesNotExist:
        return {'cart': None}
    except AttributeError:
        return {'cart': None}
