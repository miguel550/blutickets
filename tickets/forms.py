from django import forms
from  .models import Ticket


class ShowMapForm(forms.ModelForm):
    class Meta:
        model = Ticket

        fields = ['map_position']
