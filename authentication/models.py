from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField()

    def __str__(self):
        return f'{self.name}, level: {self.level}'
