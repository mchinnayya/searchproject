from django.db import models

# Create your models here.


class Branch(models.Model):
    branch_name = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=255)

    def __str__(self):
        return self.branch_name
