from django.contrib.auth import get_user_model
from django.db import models

from portal.branch.models import Branch, Promotion
from portal.dish.models import Dish
from portal.restaurant.models import DeliveryType

User = get_user_model()


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    position_order = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.name}, position order: {self.position_order}'


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=True, null=True)
    total_cost = models.FloatField()
    client = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    dishes = models.ManyToManyField(Dish, through='OrderDish')
    promotions = models.ManyToManyField(Promotion, through='OrderPromotion')


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
