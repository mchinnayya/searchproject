from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.IntegerField(default=True)  # 1 means Active, 0 means Inactive
    role = models.IntegerField() # 0 means Admin, 1 User

