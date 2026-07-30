from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
        phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
        name = models.CharField(max_length=255, null=True, blank=True)
        last_name = models.CharField(max_length=255, null=True, blank=True)
        category = models.ForeignKey( "UMS.UserCategory",related_name="users",on_delete=models.CASCADE,null=True,blank=True)
        is_admin = models.BooleanField(
            default=False
        )
        def __str__(self):
            if self.phone_number:
                return self.phone_number
            if self.username:
                return self.username
            return f"User #{self.pk}"


