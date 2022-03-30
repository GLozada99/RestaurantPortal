from django.db import models


class FoodType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'FoodType: {self.name}'


class DeliveryType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'DeliveryType: {self.name}'
