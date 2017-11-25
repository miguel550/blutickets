# Create your tasks here
from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader
from celery import shared_task
import requests


@shared_task
def send_email_notification(cleaned_data):
    c = {
        'content': cleaned_data['content']
    }
    email = EmailMultiAlternatives(
                f"Contacto: {cleaned_data['contact_name']}",  # noqa: E901
                loader.get_template(
                    'email_templates/email_contact_sent.html'
                ).render(c),
                bcc=(settings.SLACK_EMAIL,),
                reply_to=(cleaned_data['contact_email'],),
                to=[settings.CONTACT_EMAIL]
            )
    email.content_subtype = "html"
    email.send()


@shared_task
def send_slack_notification(cleaned_data):
    contact_webhook = settings.CONTACT_SLACK_CHANNEL
    requests.post(contact_webhook, json={

        "username": "ContactBot",
        "icon_emoji": ":man_in_business_suit_levitating:",
        "attachments": [
            {
                "fallback": "Alguien intenta contactarse con nosotros!",
                "pretext": "Alguien intenta contactarse con nosotros!",
                "color": "#89bdd3",
                "fields": [
                    {
                        "title": "Nombre",
                        "value": cleaned_data['contact_name'],
                        "short": False
                    },
                    {
                        "title": "Email",
                        "value": cleaned_data['contact_email'],
                        "short": False
                    },
                    {
                        "title": "Mensaje",
                        "value": cleaned_data['content'],
                        "short": False
                    },
                ],
            }
        ]
    })
