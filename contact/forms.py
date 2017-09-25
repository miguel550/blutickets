from django import forms
from django.conf import settings
from . import tasks


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
        if settings.USE_CELERY:
            tasks.send_email_notification.delay(self.cleaned_data)
        else:
            tasks.send_email_notification(self.cleaned_data)

    def _send_slack_notification(self):
        if settings.USE_CELERY:
            tasks.send_slack_notification.delay(self.cleaned_data)
        else:
            tasks.send_slack_notification(self.cleaned_data)
