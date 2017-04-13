from django import forms
from .models import Kids


class RegisterKidForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput, label='Birth Date')

    class Meta:
        model = Kids
        fields = [
            'first_name',
            'birth_date'
        ]
