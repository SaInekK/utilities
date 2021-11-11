from django.urls import path

from .views import *


urlpatterns = [
    path('', PassGenView.as_view(), name='home'),
    path('add_password/', AddPassView.as_view(), name='add'),
    path('control_panel/', ControlPanelView.as_view(), name='control_panel'),
    path('search/', SearchPassView.as_view(), name='search'),
    path('<pk>/', PasswordDetailView.as_view(), name="detail"),
    # path('password', PassWordView.as_view(), name='password')
]
