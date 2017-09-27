from django.conf import settings


def ga_tracking_id(request):
    return {
        'ga_tracking_id': settings.GA_TRACKING_ID,
        'ga_tracking_logged_in_id': settings.GA_TRACKING_LOGGED_IN_ID,
        'ga_tracking_anonymous_users_id': settings.GA_TRACKING_ANONYMOUS_USERS_ID,
    }


def use_ga(request):
    return {'use_ga': settings.USE_GA}
