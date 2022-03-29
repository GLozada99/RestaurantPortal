from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.name}, level: {self.level}'


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
