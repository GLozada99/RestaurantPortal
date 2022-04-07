from django.db import models

from dish.models import Dish, Ingredient
from restaurant.models import Restaurant


class Branch(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    front_picture = models.ImageField(
        upload_to='branch_front_pictures/', null=True, blank=True,
    )
    available_ingredients = models.ManyToManyField(
        Ingredient,
        through='Inventory',
    )

    def __str__(self):
        return f'{self.restaurant}\n{self.address}'


class Inventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    stock = models.FloatField()
    unit = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['branch', 'ingredient'],
                name='branch_ingredient',
            ),
        ]


class Promotion(models.Model):
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    branches = models.ManyToManyField(Branch)
    dishes = models.ManyToManyField(Dish, through='Combo')

    def __str__(self):
        return f'{self.name}'


class Combo(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['promotion', 'dish'],
                name='promotion_dish',
            ),
        ]
