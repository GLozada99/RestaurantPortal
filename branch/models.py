from django.db import models

from dish.models import Ingredient
from restaurant.models import Restaurant


class Branch(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    front_picture = models.ImageField(
        upload_to='branch_front_pictures/', null=True, blank=True
    )

    def __str__(self):
        return f'{self.restaurant}\n{self.address}'


class Inventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    stock = models.FloatField()
    unit = models.CharField(max_length=20)
