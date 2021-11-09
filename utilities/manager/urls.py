from django.urls import path

from .views import *


urlpatterns = [
    path('', PassGenView.as_view(), name='home'),
    path('add_password/', AddPassView.as_view(), name='add'),
    # path('password', PassWordView.as_view(), name='password')
]
