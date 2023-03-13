from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
