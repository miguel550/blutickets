from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from . import forms


class ContactFormView(FormView):
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.send_slack_notification()
        messages.success(self.request, 'Mensaje de contacto enviado, te contactaremos lo más pronto posible.')
        return super().form_valid(form)
