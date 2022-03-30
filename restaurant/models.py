from django.db import models


class FoodType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'FoodType: {self.name}'


class DeliveryType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'DeliveryType: {self.name}'


class Restaurant(models.Model):
    name = models.CharField(max_length=50, unique=True)
    food_type = models.ForeignKey(FoodType, on_delete=models.PROTECT)
    active_branches = models.IntegerField()
    active_administrators = models.IntegerField()
    is_active = models.BooleanField(default=True)
    delivery_types = models.ManyToManyField(DeliveryType)

    def __str__(self):
        return f'Restaurant: {self.name} - {self.food_type} - {self.is_active}'
