from django.db.models import Model
from rest_framework.serializers import ValidationError

from portal.branch.models import Branch, Promotion
from portal.dish.models import Dish
from portal.restaurant.models import Restaurant


class Validators:
    """Class to handle validations."""

    @staticmethod
    def validate_greater_than_zero(value):
        """Validate that the entered value is greater than zero."""
        if value <= 0:
            raise ValidationError('This field must be greater than zero.')
        return value

    @staticmethod
    def validate_greater_than_or_equal_to_zero(value):
        """Validate that the entered value is greater than or equal to zero."""
        if value < 0:
            raise ValidationError(
                'This field must be greater than or equal to zero.'
            )
        return value

    @staticmethod
    def validate_list(value):
        """Validate that the entered list isn't empty."""
        if not value:
            raise ValidationError('This field cannot be empty.')
        return value

    @staticmethod
    def validate_unique(model: Model, **kwargs):
        """Validates unique constraint of one or more fields"""
        if model.objects.filter(**kwargs).exists():
            parameters = ', '.join(list(kwargs.keys()))
            raise ValidationError({
                'non_field_errors': [
                    f'The fields {parameters} must make a unique set.'
                ]
            })

    @staticmethod
    def validate_unique_id_in_list(instances, model_field, model_name):
        """Validate that the ids in instances are unique from each other."""
        ids = []
        for instance in instances:
            if instance[model_field].id in ids:
                raise ValidationError({
                    'non_field_errors': [
                        f'The fields {model_field}, {model_name} must make a '
                        'unique set.'
                    ]
                })
            ids.append(instance[model_field].id)

    @staticmethod
    def validate_create_new_restaurant_manager(restaurant_id):
        """Validate if another restaurant manager can be created."""
        restaurant = Restaurant.objects.get(id=restaurant_id)
        active_managers = restaurant.employeeprofile_set.all().count()
        if active_managers == restaurant.active_administrators:
            raise ValidationError({
                'non_field_errors': [
                    'This restaurant reached the maximum capacity of '
                    'administrators.'
                ]
            })

    @staticmethod
    def validate_active_restaurant_managers(restaurant, quantity):
        """
        Validate that the active_administrators field has not reached the
        limit.
        """
        active_managers = restaurant.employeeprofile_set.all().count()
        return active_managers > quantity

    @staticmethod
    def validate_create_new_branch_manager(branch_id):
        """Validate if another branch manager can be created."""
        branch = Branch.objects.get(id=branch_id)
        if branch.employeeprofile_set.all().exists():
            raise ValidationError({
                'non_field_errors':
                    ['This branch already has a branch manager.']
            })

    @staticmethod
    def validate_create_new_branch(restaurant_id):
        """Validate if another branch can be created."""
        restaurant = Restaurant.objects.get(id=restaurant_id)
        branches = restaurant.branch_set.all().count()
        if branches == restaurant.active_branches:
            raise ValidationError({
                'non_field_errors': [
                    'This restaurant reached the maximum capacity of branches.'
                ]
            })

    @staticmethod
    def validate_restaurant_in_model(instance, restaurant_id, model_name):
        if instance.restaurant_id != restaurant_id:
            raise ValidationError({
                'non_field_errors': [f'{model_name} not available.']
            })

    @staticmethod
    def validate_active_branches(restaurant, quantity):
        """
        Validate that the active_branches field has not reached the limit.
        """
        active_branches = restaurant.branch_set.all().count()
        return active_branches > quantity

    @staticmethod
    def is_dish_available(
        branch: Branch, dish: Dish, dishes_quantity: int = 1
    ):
        dish_ingredients = dish.dishingredient_set.all()
        for ingredient_data in dish_ingredients:
            branch_inventory_ingredient = branch.inventory_set.get(
                ingredient=ingredient_data.ingredient
            )
            if(branch_inventory_ingredient.stock <
               (ingredient_data.quantity * dishes_quantity)):
                return False
        return True

    @classmethod
    def is_promotion_available(
        cls, branch: Branch, promotion: Promotion, promotions_quantity: int = 1
    ):
        combo_data = promotion.combo_set.all()
        for combo in combo_data:
            if not cls.is_dish_available(
                    branch, combo.dish, combo.quantity * promotions_quantity):
                return False
        return True
