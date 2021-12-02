from django import forms
from django.forms import fields, widgets
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import PasswordModel


class DateInput(forms.DateInput):
    input_type = 'date'


class CreatePasswordForm(forms.ModelForm):
    class Meta:
        model = PasswordModel
        fields = ['password', 'used_for_website', 'retired_date', 'description']
        widgets = {
            'retired_date': DateInput(format='%d%m%Y'),
            'password': forms.PasswordInput(attrs={'autocomplete': 'off', 'data-toggle': 'password'})
        }


class GeneratePasswordForm(forms.Form):
    CHOICES = ((i, str(i)) for i in range(8, 33, 2))

    length = forms.CharField(label="Password length", widget=forms.Select(choices=CHOICES))
    has_letters = forms.BooleanField(label="Letters", widget=forms.CheckboxInput, required=True)
    has_uppercase = forms.BooleanField(label="Uppercase", widget=forms.CheckboxInput, required=False)
    has_punctuation = forms.BooleanField(label="Punctuation", widget=forms.CheckboxInput, required=False)
    has_numbers = forms.BooleanField(label="Numbers", widget=forms.CheckboxInput, required=False)
