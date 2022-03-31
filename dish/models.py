from django.db import models

from restaurant.models import Restaurant


class Ingredient(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.name}'


class DishCategory(models.Model):
    name = models.CharField(max_length=60)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'restaurant'],
                name='restaurant_dish_category'
            )
        ]

    def __str__(self):
        return f'{self.name}'
