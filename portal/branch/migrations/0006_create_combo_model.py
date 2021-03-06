# Generated by Django 3.2.12 on 2022-04-02 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0005_add_restaurant_to_ingredient_model'),
        ('branch', '0005_create_promotion_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Combo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dish.dish')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch.promotion')),
            ],
        ),
        migrations.AddConstraint(
            model_name='combo',
            constraint=models.UniqueConstraint(fields=('promotion', 'dish'), name='promotion_dish'),
        ),
    ]
