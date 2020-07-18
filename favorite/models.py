from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from contact.models import Contact


class Favorite(models.Model):
    favorite_name = models.CharField(max_length=255)
    favorite_description = models.CharField(max_length=255)

    # def __str__(self):
    #     return self.favorite_name


class Favorite_link_with_contact(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,null=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    # def __str__(self):
    #     return self.favorite
