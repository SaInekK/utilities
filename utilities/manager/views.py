from django.shortcuts import render

# Create your views here.
import string
from django.shortcuts import render
from django.views import View
import random
from .forms import *
from django.contrib import messages
from django.utils import timezone
# Create your views here.


class PassGenView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'manager/home.html', {'form': GeneratePasswordForm()})

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
        return render(request, 'manager/home.html', {'form': form, 'password': password})


class AddPassView(View):
    def get(self, request, *args, **kwargs):
        kwargs['form'] = CreatePasswordForm()
        return render(request, "manager/add_password.html", kwargs)

    def post(self, request, *args, **kwargs):
        form = CreatePasswordForm(data=request.POST)
        passwd = request.POST.get('passwd')
        kwargs['passwd'] = passwd
        if form.is_valid():
            #get fields
            password = form.cleaned_data.get('password')
            retired_date = form.cleaned_data.get('retired_date')
            used_for_website = form.cleaned_data.get('used_for_website')
            description = form.cleaned_data.get('description')

            #Check if there is a same password
            if PasswordModel.objects.filter(password=password):
                messages.warning(request, f"The password is already used on a platform")
                kwargs['form'] = CreatePasswordForm()
            else:
                # save them into database
                obj = PasswordModel.objects.create(
                    password=password,
                    created_date=timezone.now(),
                    retired_date=retired_date,
                    used_for_website=used_for_website,
                    description=description)
                messages.success(request, f"New password was created successfully. The password will be retired on")
                kwargs['form'] = CreatePasswordForm()
                kwargs['object'] = obj
        else:
            kwargs['form'] = CreatePasswordForm()
        return render(request, "manager/add_password.html", kwargs)
