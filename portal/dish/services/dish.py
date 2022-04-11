from django.db.transaction import atomic
from rest_framework.serializers import ValidationError

from portal.branch.models import Branch
from portal.dish.models import Dish, DishCategory, DishIngredient
from portal.validators import Validators


class DishAPIService:

    @classmethod
    @atomic
    def create(cls, data: dict, restaurant_id: int, category_id: int):
        ingredients_data = data.pop('ingredients')
        ValidateDishAPIService.validate_data(
            data['name'], category_id, restaurant_id, ingredients_data,
        )
        dish = cls.get_instance(data, category_id)
        cls.create_dish_ingredients(dish, ingredients_data)
        return dish

    @staticmethod
    def get_instance(data, category_id):
        dish = Dish(
            name=data['name'],
            price=data['price'],
            description=data.get('description'),
            category_id=category_id,
            picture=data.get('picture'),
        )
        dish.save()
        return dish

    @staticmethod
    def create_dish_ingredients(dish: Dish, ingredients_data):
        dish_ingredients = [
            DishIngredient(
                dish_id=dish.id,
                ingredient_id=dish_ingredient['ingredient'].id,
                quantity=dish_ingredient['quantity'],
                unit=dish_ingredient['unit'],
            ) for dish_ingredient in ingredients_data
        ]
        DishIngredient.objects.bulk_create(dish_ingredients)


class ValidateDishAPIService:

    @classmethod
    def validate_data(cls, name, category_id, restaurant_id, dish_ingredients):
        Validators.validate_unique(
            Dish, name=name, category_id=category_id,
        )
        Validators.validate_unique_id_in_list(
            dish_ingredients, 'ingredient', 'dish',
        )
        cls.validate_ingredients(restaurant_id, dish_ingredients)

    @staticmethod
    def validate_ingredients(restaurant_id, dish_ingredients):
        for dish_ingredient in dish_ingredients:
            if dish_ingredient['ingredient'].restaurant_id != restaurant_id:
                raise ValidationError({
                    'ingredients': 'Invalid ingredients.'
                })


class AvailableDishesAPIService:

    @staticmethod
    def get_available_dishes(category_id: int, branch_id: int):
        category = DishCategory.objects.get(pk=category_id)
        branch = Branch.objects.get(pk=branch_id)
        dishes = category.dish_set.all()
        return [
            dish for dish in dishes if Validators.is_dish_available(
                branch, dish,
            )
        ]
