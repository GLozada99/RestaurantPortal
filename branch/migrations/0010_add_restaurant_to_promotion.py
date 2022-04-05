# Generated by Django 3.2.12 on 2022-04-04 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_create_dish_category_model'),
        ('branch', '0009_change_ingredients_avalilable_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='restaurant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
            preserve_default=False,
        ),
    ]
