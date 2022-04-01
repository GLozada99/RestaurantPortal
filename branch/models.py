from django.db import models

from restaurant.models import Restaurant


class Branch(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    front_picture = models.ImageField(
        upload_to='branch_front_pictures/', null=True, blank=True
    )

    def __str__(self):
        return f'{self.restaurant}\n{self.address}'
