import datetime

from django.db import models

# Create your models here.


class PasswordModel(models.Model):
    password = models.CharField(max_length=32, null=True, blank=False)
    created_date = models.DateField()
    retired_date = models.DateField(null=False, blank=False)
    used_for_website = models.CharField(max_length=63)
    description = models.TextField(max_length=254)
