from django import forms
from .models import Kid


class RegisterKidForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput, label='Birth Date')

    class Meta:
        model = Kid
        fields = [
            'first_name',
            'birth_date'
        ]
