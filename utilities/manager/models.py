from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PasswordModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=False)
    created_date = models.DateField()
    retired_date = models.DateField(null=False, blank=False)
    used_for_website = models.CharField(max_length=63)
    description = models.TextField(max_length=254)
