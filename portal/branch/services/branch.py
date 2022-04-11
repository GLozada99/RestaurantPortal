from django.db.transaction import atomic

from portal.branch.models import Branch


class BranchAPIService:

    @classmethod
    @atomic
    def create(cls, data: dict, restaurant_id):
        branch = cls.get_instance(data, restaurant_id)
        return branch

    @classmethod
    def get_instance(cls, data: dict, restaurant_id: int) -> Branch:
        branch = Branch(
            restaurant_id=restaurant_id,
            address=data['address'],
            phone_number=data['phone_number'],
            front_picture=data.get('front_picture'),
        )
        branch.save()
        return branch
