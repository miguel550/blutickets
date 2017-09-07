from django import forms
from django.contrib.auth import get_user_model
from .models import Province, Sector
from operator import methodcaller


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


class SignUpForm(forms.ModelForm):

    province = forms.TypedChoiceField(choices=get_province_choices(),
                                      initial=get_user_model().DISTRITO_NACIONAL,
                                      label="Provincia")
    sector = forms.TypedChoiceField(choices=get_sector_choices(),
                                    coerce=lambda x: Sector.objects.get(pk=x),
                                    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.sector = self.cleaned_data['sector']
        user.save()

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'province', )
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),

        }
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
        }



