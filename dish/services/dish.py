from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from branch.models import Branch
from dish.models import Dish, DishCategory, DishIngredient
from dish.serializers.dish import (
    BasicDishSerializer,
    DetailedDishWithIngredientsSerializer,
    DishSerializer,
)
from portal.validators import Validators


class DishAPIService:

    @classmethod
    @atomic
    def create(
        cls, serializer: DishSerializer, category_id: int, restaurant_id: int
    ) -> Response:
        ingredients_data = serializer.validated_data.pop('ingredients')
        cls.validate_data(
            serializer.validated_data['name'],
            category_id,
            restaurant_id,
            ingredients_data,
        )
        serializer.save(category_id=category_id)
        cls.create_dish_ingredients(serializer, ingredients_data)
        cls.update_response_data(serializer, ingredients_data)
        return Response(
            DetailedDishWithIngredientsSerializer(
                serializer.validated_data,
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def create_dish_ingredients(serializer: DishSerializer, ingredients_data):
        dish_ingredients = [
            DishIngredient(
                dish_id=serializer.data['id'],
                ingredient_id=dish_ingredient['ingredient'].id,
                quantity=dish_ingredient['quantity'],
                unit=dish_ingredient['unit'],
            ) for dish_ingredient in ingredients_data
        ]
        DishIngredient.objects.bulk_create(dish_ingredients)

    @staticmethod
    def update_response_data(serializer: DishSerializer, ingredients_data):
        serializer.validated_data['ingredients'] = ingredients_data
        serializer.validated_data['id'] = serializer.data['id']

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

    @staticmethod
    def is_dish_available(branch: Branch, dish: Dish):
        dish_ingredients = dish.dishingredient_set.all()
        for ingredient_data in dish_ingredients:
            branch_inventory_ingredient = branch.inventory_set.get(
                ingredient=ingredient_data.ingredient)
            if branch_inventory_ingredient.stock < ingredient_data.quantity:
                return False
        return True

    @classmethod
    def get_available_dishes_category_branch(
            cls, category: DishCategory, branch: Branch,
    ):
        dishes = category.dish_set.all()
        available_dishes = [dish for dish in dishes if
                            cls.is_dish_available(branch, dish)]
        return available_dishes

    @classmethod
    def get_available_dishes_branch(cls, branch_id: int):
        branch = Branch.objects.get(pk=branch_id)
        restaurant = branch.restaurant
        restaurant_categories = restaurant.dishcategory_set.all()
        available_dishes = []
        for category in restaurant_categories:
            available_dishes.extend(
                cls.get_available_dishes_category_branch(category, branch)
            )
        serializer = BasicDishSerializer(data=available_dishes, many=True)
        serializer.is_valid()
        return Response(serializer.data)
