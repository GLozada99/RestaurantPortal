from django.contrib.auth import get_user_model
from django.db import models

from branch.models import Branch, Promotion
from dish.models import Dish

User = get_user_model()


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    dishes = models.ManyToManyField(Dish, through='OrderDish')
    promotions = models.ManyToManyField(Promotion, through='OrderPromotion')
    total_cost = models.FloatField()


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'dish'],
                name='order_dish_unique_constraint',
            ),
        ]


class OrderPromotion(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'promotion'],
                name='order_promotion_unique_constraint',
            ),
        ]
