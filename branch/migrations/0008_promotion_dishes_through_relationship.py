# Generated by Django 3.2.12 on 2022-04-03 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0006_dish_ingredients_through_relationship'),
        ('branch', '0007_branch_inventory_through_relationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='dishes',
            field=models.ManyToManyField(through='branch.Combo', to='dish.Dish'),
        ),
    ]
