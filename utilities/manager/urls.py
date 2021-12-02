from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('', PassGenView.as_view(), name='home'),
    path('add_password/', AddPassView.as_view(), name='add'),
    path('control_panel/', ControlPanelView.as_view(), name='control_panel'),
    path('search/', SearchPassView.as_view(), name='search'),
    path('<pk>/', PasswordDetailView.as_view(), name="details"),
    path('update/<pk>/', PasswordUpdateView.as_view(), name="update"),
    path('delete/<pk>/', PasswordDeleteView.as_view(), name="delete"),
]
