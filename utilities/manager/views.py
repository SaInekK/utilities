import datetime

import transliterate
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect

import string
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
import random

from django.views.generic import DetailView, UpdateView, DeleteView, FormView, ListView

from .forms import *
from django.contrib import messages
from django.utils import timezone


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'manager/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('control_panel')


class RegisterView(FormView):
    template_name = 'manager/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('control_panel')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('control_panel')
        return super(RegisterView, self).get(*args, **kwargs)


class PassGenView(LoginRequiredMixin, View):
    login_url = "login"

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


class AddPassView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, *args, **kwargs):
        kwargs['form'] = CreatePasswordForm()
        return render(request, "manager/add_password.html", kwargs)

    def post(self, request, *args, **kwargs):
        form = CreatePasswordForm(data=request.POST)
        passwd = request.POST.get('passwd')
        kwargs['passwd'] = passwd
        if form.is_valid():
            user = self.request.user
            password = form.cleaned_data.get('password')
            retired_date = form.cleaned_data.get('retired_date')
            used_for_website = form.cleaned_data.get('used_for_website')
            description = form.cleaned_data.get('description')

            # Check if there is the same password
            if PasswordModel.objects.filter(password=password):
                messages.warning(request, f"The password is already used on a platform")
                kwargs['form'] = CreatePasswordForm()
            else:
                obj = PasswordModel.objects.create(
                    user=user,
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


class SearchPassView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if not query:
            query = ""
        pass_obj = PasswordModel.objects.filter(
            Q(used_for_website__icontains=query) |
            Q(description__icontains=query) |
            Q(password__icontains=query)).order_by("retired_date")
        p = Paginator(pass_obj, 8)
        page_number = request.GET.get('page')
        # try:
        page_obj = p.get_page(page_number)
        '''except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)'''

        kwargs['page_obj'] = page_obj

        return render(request, "manager/search_password.html", kwargs)


class ControlPanelView(LoginRequiredMixin, ListView):
    login_url = "login"
    model = PasswordModel

    def get(self, request, *args, **kwargs):
        qs = PasswordModel.objects.filter(user=self.request.user).order_by('-id')
        p = Paginator(qs, 5)
        page_number = self.request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty return last page
            page_obj = p.page(p.num_pages)
        now = timezone.now()
        end_date = now + datetime.timedelta(days=15)
        closest_date = PasswordModel.objects.filter(
            Q(user=self.request.user) &
            Q(retired_date__gte=now)).order_by('retired_date').first()
        notifications = PasswordModel.objects.filter(
            Q(user=self.request.user) &
            Q(retired_date__range=[now, end_date]))

        last_item = PasswordModel.objects.last()
        kwargs = kwargs | {
            'last_item': last_item,
            'closest_date': closest_date,
            'records': qs.count(),
            'page_obj': page_obj,
            'notifications': notifications,
            'notifications_count': notifications.count(),
        }
        return render(request, "manager/control_panel.html", kwargs)


class PasswordDetailView(LoginRequiredMixin, DetailView):
    login_url = "login"
    model = PasswordModel
    template_name = "manager/password_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    model = PasswordModel
    fields = [
        "password", "used_for_website", "retired_date", "description"
    ]
    template_name = "manager/update_password.html"
    success_url = reverse_lazy("control_panel")

    def form_valid(self, form):
        messages.success(self.request, f"The record was updated!")
        return super(PasswordUpdateView, self).form_valid(form)


class PasswordDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = PasswordModel
    template_name = "manager/delete_password.html"
    success_url = reverse_lazy("control_panel")
    success_message = "The record was removed successfully!"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        data = super(PasswordDeleteView, self).delete(request, *args, **kwargs)
        messages.warning(self.request, self.success_message % obj.__dict__)
        return data


class TranslitView(LoginRequiredMixin, FormView):
    template_name = 'manager/translit.html'
    login_url = "login"

    def get(self, request, *args, **kwargs):
        text = request.GET.get('text') or ''
        kwargs['form'] = TranslitForm()
        option = self.request.GET.get('option')
        if option:
            if option == '0':
                kwargs['translated'] = transliterate.translit(text, 'ru')
            if option == '1':
                kwargs['translated'] = transliterate.translit(text, reversed=True)
        return render(request, "manager/translit.html", kwargs)
