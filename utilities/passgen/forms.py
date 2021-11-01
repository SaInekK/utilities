from django import forms
from django.forms import fields, widgets


# from .models import CreatePasswordModel
#
# class DateInput(forms.DateInput):
#     input_type = 'date'
#
# class CreatePasswordForm(forms.ModelForm):
#     class Meta:
#         model = CreatePasswordModel
#         fields = ['password', 'used_for_website', 'retired_date', 'explanation']
#         widgets = {
#             'retired_date' : DateInput(format='%d%m%Y'),
#             'password' : forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password'})
#         }


class GeneratePasswordForm(forms.Form):
    CHOICES = ((i, str(i)) for i in range(8, 33, 2))

    length = forms.CharField(label="Password Length", widget=forms.Select(choices=CHOICES))
    has_letters = forms.BooleanField(label="Letters", widget=forms.CheckboxInput, required=True)
    has_uppercase = forms.BooleanField(label="Mixed Case", widget=forms.CheckboxInput, required=False)
    has_punctuation = forms.BooleanField(label="Punctuation", widget=forms.CheckboxInput, required=False)
    has_numbers = forms.BooleanField(label="Numbers", widget=forms.CheckboxInput, required=False)
