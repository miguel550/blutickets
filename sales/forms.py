from django import forms
from django.contrib.auth import get_user_model
from .models import Address, LineItem
from profiles.models import Province, Sector
from django_select2.forms import Select2Widget


def get_province_choices():
    try:
        return Province.objects.filter(active=True)
    except:
        return [(0, 'No hay provincias')]


class LineItemForm(forms.ModelForm):

    class Meta:
        model = LineItem
        fields = ('quantity',)


class OrderFirstStepForm(forms.Form):
    pass


class OrderSecondStepForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].widget = Select2Widget(
            attrs={
                'class': 'form-control'
            },
        )
        self.fields['sector'].queryset = Sector.objects.filter(active=True)
        self.fields['sector'].empty_label = 'Elija su sector'

    class Meta:
        model = Address
        fields = (
            'sector',
            'street_and_house',
            'reference'
        )
        widgets = {
            'street_and_house': forms.TextInput(
                attrs={
                    'placeholder': "Calle, número, casi esquina.",
                    'class': 'form-control',
                    'style': "width: -webkit-fill-available;",
                }
            ),
            'reference': forms.TextInput(
                attrs={
                    'placeholder': "Al lado de, Frente a, etc.",
                    'style': "width: -webkit-fill-available;",
                    'class': 'form-control',
                }
            )
        }
        labels = {
            'street_and_house': 'Dirección',
            'reference': "Referencias",
        }


class OrderSecondStepFormPhones(forms.ModelForm):
    """
    phone_number_primary_type = forms.ChoiceField(choices=(
                                                ('', '--Contacto--'),
                                                ('phone', 'Teléfono'),
                                                ('cellphone', 'Celular')
                                               ),
                                      initial=''
                                      )"""
    phone_number_primary = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                    'placeholder': 'Ej: 809 555 5555',
                    'class': 'form-control',
                }
        ),
        label='Número de teléfono primario'
    )
    """
    phone_number_secondary_type = forms.ChoiceField(choices=(
                                                ('', '--Contacto Adicional--'),
                                                ('phone', 'Teléfono'),
                                                ('cellphone', 'Celular')
                                               ),
                                      initial='',
                                        required=False
                                      )"""
    phone_number_secondary = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                    'placeholder': 'Teléfono opcional.',
                    'class': 'form-control'
                }
                ),
        label='Número de teléfono secundario'
    )

    def save(self, commit=True):
        user = self.instance
        # user.phone_number_primary_type = self.cleaned_data['phone_number_primary_type']
        user.phone_number_primary = self.cleaned_data['phone_number_primary']
        # user.phone_number_secondary_type = self.cleaned_data['phone_number_secondary_type']
        user.phone_number_secondary = self.cleaned_data['phone_number_secondary']
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            # 'phone_number_primary_type',
            'phone_number_primary',
            # 'phone_number_secondary_type',
            'phone_number_secondary',
        )
