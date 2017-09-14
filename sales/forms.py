from django import forms
from django.contrib.auth import get_user_model
from .models import Order, Address, LineItem
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


class LineItemForm(forms.ModelForm):

    class Meta:
        model = LineItem
        fields = ('quantity',)


class OrderFirstStepForm(forms.Form):
    pass


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


class OrderSecondStepFormPhones(forms.ModelForm):
    phone_number_primary_type = forms.ChoiceField(choices=(
                                                ('', '--Contacto--'),
                                                ('phone', 'Teléfono'),
                                                ('cellphone', 'Celular')
                                               ),
                                      initial=''
                                      )
    phone_number_primary = forms.CharField(max_length=15,
                                   widget=forms.TextInput(
                                       attrs={
                                            'placeholder': 'Ej: 809 555 5555'
                                       })
                                   )
    phone_number_secondary_type = forms.ChoiceField(choices=(
                                                ('', '--Contacto Adicional--'),
                                                ('phone', 'Teléfono'),
                                                ('cellphone', 'Celular')
                                               ),
                                      initial='',
                                        required=False
                                      )
    phone_number_secondary = forms.CharField(max_length=15,
                                             required=False,
                                             widget=forms.TextInput(
                                             attrs={
                                                'placeholder': 'Teléfono opcional.'
                                             })
                                             )

    def save(self, commit=True):
        user = self.instance
        user.phone_number_primary_type = self.cleaned_data['phone_number_primary_type']
        user.phone_number_primary = self.cleaned_data['phone_number_primary']
        user.phone_number_secondary_type = self.cleaned_data['phone_number_secondary_type']
        user.phone_number_secondary = self.cleaned_data['phone_number_secondary']
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'phone_number_primary_type',
            'phone_number_primary',
            'phone_number_secondary_type',
            'phone_number_secondary',
        )
