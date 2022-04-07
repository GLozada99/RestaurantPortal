from django.db.models import Model
from rest_framework.serializers import ValidationError

from restaurant.models import Restaurant


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
                'non_field_errors':
                    f'The fields {parameters} must make a unique set.'
            })

    @staticmethod
    def validate_unique_id_in_list(instances, model_field, model_name):
        """Validate that the ids in instances are unique from each other."""
        ids = []
        for instance in instances:
            if instance[model_field].id in ids:
                raise ValidationError({
                    'non_field_errors':
                        [
                            f'The fields {model_field}, {model_name} must make'
                            ' a unique set.'
                        ]
                })
            ids.append(instance[model_field].id)

    @staticmethod
    def validate_create_new_restaurant_manager(restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        active_managers = restaurant.employeeprofile_set.all().count()
        if active_managers == restaurant.active_administrators:
            raise ValidationError({
                'non_field_errors':
                    [
                        'This restaurant reached the maximum capacity of '
                        'administrators.'
                    ]
            })

    @staticmethod
    def validate_active_restaurant_managers(restaurant, quantity):
        active_managers = restaurant.employeeprofile_set.all().count()
        if active_managers > quantity:
            return True
        return False

    @staticmethod
    def validate_create_new_branch(restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        branches = restaurant.branch_set.all().count()
        if branches == restaurant.active_branches:
            raise ValidationError({
                'non_field_errors':
                    [
                        'This restaurant reached the maximum capacity of '
                        'branches.'
                    ]
            })

    @staticmethod
    def validate_active_branches(restaurant, quantity):
        active_branches = restaurant.branch_set.all().count()
        if active_branches > quantity:
            return True
        return False
