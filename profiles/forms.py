from django import forms
from django.contrib.auth import get_user_model


class SignUpForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        self.fields['sector'].widget = Select2Widget(attrs={'data-placeholder': 'Elija su sector'})
        self.fields['sector'].queryset = Sector.objects.filter(active=True)
        self.fields['sector'].empty_label = "---Sector---"
        """

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # user.sector_id = self.cleaned_data['sector']
        user.save()

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            # 'sector',
            # 'select_number_primary',
            # 'phone_number_primary',
            # 'select_number_secondary',
            # 'phone_number_secondary',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),

        }
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
        }
