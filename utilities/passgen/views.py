from django.shortcuts import render

# Create your views here.
import string
from django.shortcuts import render
from django.views import View
import random
from .forms import *
# Create your views here.


class PassGenView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'passgen/home.html', {'form': GeneratePasswordForm()})

    def post(self, request, *args, **kwargs):
        lower_letters = string.ascii_lowercase
        upper_letters = string.ascii_uppercase
        symbols = string.punctuation
        numbers = string.digits
        form = GeneratePasswordForm(data=request.POST)
        if form.is_valid():
            password_length = int(form.cleaned_data.get('length'))
            has_letters = form.cleaned_data.get('has_letters')
            has_upper_letters = form.cleaned_data.get('has_uppercase')
            has_punctuation = form.cleaned_data.get('has_punctuation')
            has_numbers = form.cleaned_data.get('has_numbers')
            characters = []
            if has_upper_letters:
                characters.extend(upper_letters)
            if has_punctuation:
                characters.extend(symbols)
            if has_numbers:
                characters.extend(numbers)
            if has_letters:
                characters.extend(lower_letters)
            temp = random.choices(characters, k=password_length)
            password = ''.join(temp)
        return render(request, 'passgen/home.html', {'form': form, 'password': password})


# class PassWordView(View):
#     def get(self, request, *args, **kwargs):
#         lower = list(ascii_lowercase)
#         upper = list(ascii_uppercase)
#         length = int(request.GET.get('length'))
#
#         password = ''.join([random.choice(lower) for i in range(length)])
#
#         return render(request, 'passgen/password.html', {'password': password})
