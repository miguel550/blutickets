from django import forms
from django.contrib.auth import get_user_model
from .models import Order, Address
from profiles.models import Province, Sector


def get_province_choices():
    try:
        return Province.objects.filter(active=True)
    except:
        return [(0, 'No hay provincias')]


def get_sector_choices():
    try:
        return Sector.objects.filter(active=True)
    except:
        return [(0, 'No hay sector')]


class OrderFirstStepForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('user', 'line_items')


class OrderSecondStepForm(forms.ModelForm):
    province = forms.ModelChoiceField(
        queryset=get_province_choices(),
        initial=get_user_model().DISTRITO_NACIONAL,
        label="Provincia",
    )
    sector = forms.ModelChoiceField(
        queryset=get_sector_choices(),
        empty_label="--Sector--"
    )
    street_and_house = forms.CharField(
        max_length=100,
        label="Calle",
        widget=forms.TextInput(
            attrs={
                'placeholder': " (Calle/Casa/apart,etc)",
            }
        ),
    )
    reference = forms.CharField(
        max_length=100,
        label="Referencias",
        widget=forms.TextInput(
            attrs={
                'placeholder': "(Al lado de/Frente a/etc)",
            }
        ),
    )

    def save(self, commit=True):
        order = super().save(commit=commit)
        order.address = Address.objects.create(
            sector=self.cleaned_data['sector'],
            street_and_house=self.cleaned_data['street_and_house'],
            reference=self.cleaned_data['reference'],
        )
        order.save()
        return order

    class Meta:
        model = Order
        fields = ('province',)
