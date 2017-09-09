from django import forms
from django.contrib.auth import get_user_model
from .models import Province, Sector
from operator import methodcaller


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


class SignUpForm(forms.ModelForm):

    province = forms.ModelChoiceField(queryset=get_province_choices(),
                                      initial=get_user_model().DISTRITO_NACIONAL,
                                      label="Provincia")
    sector = forms.ModelChoiceField(queryset=get_sector_choices(),
                                    empty_label="--Sector--")
    select_number_primary = forms.ChoiceField(choices=(
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
    select_number_secondary = forms.ChoiceField(choices=(
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

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.sector_id = self.cleaned_data['sector']
        user.phone_number_primary_type = self.cleaned_data['select_number_primary']
        user.phone_number_primary = self.cleaned_data['phone_number_primary']
        user.phone_number_secondary_type = self.cleaned_data['select_number_secondary']
        user.phone_number_secondary = self.cleaned_data['phone_number_secondary']
        user.save()

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'province',
            'sector',
            'select_number_primary',
            'phone_number_primary',
            'select_number_secondary',
            'phone_number_secondary',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),

        }
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
        }



