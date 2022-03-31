from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=80)
    
    def __str__(self):
        return f'{self.name}'
