from django import forms
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader
import requests


class ContactForm(forms.Form):
    contact_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }
        )
    )
    contact_email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@ejemplo.com'
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su mensaje detallado y le contactaremos.'
            }
        ),
        label="Mensaje"
    )

    def send_notifications(self):
        self._send_email_notification()
        self._send_slack_notification()

    def _send_email_notification(self):
        c = {
            'content': self.cleaned_data['content']
        }
        email = EmailMultiAlternatives(
            f"Contacto: {self.cleaned_data['contact_name']}",
            loader.get_template(
                'email_templates/email_contact_sent.html'
            ).render(c),
            bcc=(settings.SLACK_EMAIL,),
            reply_to=(self.cleaned_data['contact_email'],),
            to=[settings.CONTACT_EMAIL]
        )
        email.content_subtype = "html"
        email.send()

    def _send_slack_notification(self):
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
                            "value": self.cleaned_data['contact_name'],
                            "short": False
                        },
                        {
                            "title": "Email",
                            "value": self.cleaned_data['contact_email'],
                            "short": False
                        },
                        {
                            "title": "Mensaje",
                            "value": self.cleaned_data['content'],
                            "short": False
                        },
                    ],
                }
            ]
        })
