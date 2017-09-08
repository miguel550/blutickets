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
    sector = forms.ChoiceField(
        choices=get_sector_choices(),
    )
    street_and_house = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': "Dirección casa/ Calle X Casa #12",

            'class': "mx-auto"
        }),
    )
    reference = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': "Referencia/ Al lado de..., frente a...",
            'class': "mx-auto"
        }),
    )

    def save(self, commit=True):
        order = super().save(commit=commit)
        order.address = Address.objects.create(
            sector_id=self.cleaned_data['sector'],
            street_and_house=self.cleaned_data['street_and_house'],
            reference=self.cleaned_data['reference'],
        )
        order.save()
        return order

    class Meta:
        model = Order
        fields = ('province',)
