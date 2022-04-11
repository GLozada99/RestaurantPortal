from portal.branch.models import Inventory
from portal.order.models import Order


class SubtractInventoryAPIService:

    @classmethod
    def subtract(cls, order: Order):
        cls.branch_id = order.branch_id
        cls.subtract_dishes(order.orderdish_set.all())
        cls.subtract_promotions(order.orderpromotion_set.all())

    @classmethod
    def subtract_promotions(cls, order_promotions):
        for order_promotion in order_promotions:
            cls.subtract_dishes(
                order_promotion.promotion.combo_set.all(),
                order_promotion.quantity,
            )

    @classmethod
    def subtract_dishes(cls, order_dishes, quantity=1):
        for order_dish in order_dishes:
            cls.subtract_ingredients(
                order_dish.dish.dishingredient_set.all(),
                order_dish.quantity * quantity,
            )

    @classmethod
    def subtract_ingredients(cls, dish_ingredients, order_quantity):
        for dish_ingredient in dish_ingredients:
            cls.subtract_inventory(
                dish_ingredient.ingredient.inventory_set.get(
                    branch_id=cls.branch_id,
                ),
                dish_ingredient.quantity,
                order_quantity,
            )

    @staticmethod
    def subtract_inventory(
        inventory: Inventory, ingredient_quantity, order_quantity
    ):
        inventory.stock -= ingredient_quantity * order_quantity
        inventory.save()
