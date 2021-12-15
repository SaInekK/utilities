from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class TaskModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['completed']


