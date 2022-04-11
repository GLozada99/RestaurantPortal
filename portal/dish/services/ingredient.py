from portal.dish.models import Ingredient
from portal.validators import Validators


class IngredientAPIService:

    @classmethod
    def create(cls, data: dict, restaurant_id):
        cls.validate_restaurant(data['name'], restaurant_id)
        return cls.get_instance(data, restaurant_id)

    @staticmethod
    def get_instance(data, restaurant_id):
        ingredient = Ingredient(
            name=data['name'],
            restaurant_id=restaurant_id,
        )
        ingredient.save()
        return ingredient

    @staticmethod
    def validate_restaurant(name, restaurant_id):
        Validators.validate_unique(
            Ingredient, name=name, restaurant=restaurant_id,
        )
