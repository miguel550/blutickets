from django import forms
from django.contrib.auth import get_user_model
from .models import Order, Address
from profiles.models import Province, Sector


def get_province_choices():
    try:
        return map(lambda x: (*x.values(),),
                   Province.objects.filter(active=True).values('pk', 'name'))
    except:
        return [(0, 'No hay provincias')]


def get_sector_choices():
    try:
        return map(lambda x: (*x.values(),),
                   Sector.objects.filter(active=True).values('pk', 'name'))
    except:
        return [(0, 'No hay sector')]


class OrderFirstStepForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('user', 'line_items')


class OrderSecondStepForm(forms.ModelForm):
    province = forms.TypedChoiceField(choices=get_province_choices(),
                                      initial=get_user_model().DISTRITO_NACIONAL,
                                      label="Provincia")
    sector = forms.TypedChoiceField(choices=get_sector_choices(),
                                    coerce=lambda x: Sector.objects.get(pk=x),
                                    )
    street_and_house = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': "Dirección casa",

            'class': "mx-auto"
        }),
    )
    reference = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': "Referencia",
            'class': "mx-auto"
        }),
    )

    class Meta:
        model = Order
        fields = ('province',)
