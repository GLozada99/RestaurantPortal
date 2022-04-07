from django.db import models

from restaurant.models import Restaurant


class Ingredient(models.Model):
    name = models.CharField(max_length=80)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class DishCategory(models.Model):
    name = models.CharField(max_length=60)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'restaurant'],
                name='restaurant_dish_category',
            ),
        ]

    def __str__(self):
        return f'{self.name}'


class Dish(models.Model):
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(null=True)
    category = models.ForeignKey(DishCategory, on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to='dish_pictures/', null=True, blank=True,
    )
    ingredients = models.ManyToManyField(Ingredient, through='DishIngredient')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='dish_category',
            ),
        ]


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dish', 'ingredient'],
                name='dish_ingredient_unique_constraint',
            ),
        ]
