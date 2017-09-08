from django import forms
from .models import Order


class OrderFirstStepForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('user', 'line_items')


class OrderSecondStepForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('map_position',)
