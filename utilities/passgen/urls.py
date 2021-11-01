from django.urls import path

from .views import *


urlpatterns = [
    path('', PassGenView.as_view(), name='home'),
    # path('password', PassWordView.as_view(), name='password')
]
